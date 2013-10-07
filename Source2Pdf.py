#!/usr/bin/env python

"""
Source2Pdf.py
This file is part of Source2PDF

Copyright (C) 2013 - Luke Frisken

Source2PDF is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Source2PDF is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Source2PDF. If not, see <http://www.gnu.org/licenses/>.
"""


import cStringIO as StringIO
import os, os.path, sys, datetime, pwd, re
import argparse
from subprocess import Popen, PIPE, STDOUT
import ho.pisa as pisa

#import pygments

def get_current_directory():
	return os.getcwd()

def get_source_directory():
	file_path = os.path.realpath(sys.argv[0])
	return os.path.dirname(file_path) + "/"

class ProjectDocument(object):
	"""This Class Represents the document of the overall project"""
	def __init__(self, path):
		self.file_documents = []
		self.path = path
		self.get_project_stats()
		self.main_re = re.compile(".*main[.].*", re.IGNORECASE)
		
	def append(self, document):
		#TODO: make main_re part of the options
		#insert any document with path containing main at the start
		match = self.main_re.match(document.path)
		if match:
			self.file_documents.insert(0, document)
		else:
			#append any others to the end ;)
			self.file_documents.append(document)
	
	def get_project_stats(self):
		self.cloc = 0
		self.name = os.path.basename(self.path)
	
	def to_html(self):
		"""Convert document to html"""
		html = """
<html>
<style>
@page {
  margin: 1cm;
  margin-bottom: 2.5cm;
  @frame footer {
    -pdf-frame-content: footerContent;
    bottom: 1cm;
    margin-left: 1cm;
    margin-right: 1cm;
    height: 1cm;
  }
  @frame footer {
    -pdf-frame-content: headerContent;
    top: 0.5cm;
    margin-left: 17.5cm;
    margin-right: 1cm;
    height: 1cm;
  }
}
font {
	font-size: 140%;
}
</style>
<div id="footerContent">
   page <pdf:pagenumber />
</div>
"""
		html += """<div id="headerContent">
   <b>Project: {0}</b>
</div>""".format(self.name)
		html += """<h1 style="font-size:300%">Project: {0}</h1>
		""".format(self.name)
		for d in self.file_documents:
			html += d.to_html()
		
		html += "</style>"
		return html
		
	def to_pdf_file(self, filepath):
		"""Convert document to pdf file"""
		f = open(filepath, 'w')
		print("starting")
		html = self.to_html()
		#f.write(html)
		try:
			encoded_html = html.encode("ISO-8859-1")
		except:
			changed_html = self.validate_encoding(html)
			encoded_html = html
		pdf = pisa.CreatePDF(StringIO.StringIO(encoded_html), f)
		print(pdf.err)
		#if not pdf.err:
			#pisa.startViewer(filepath)
		f.close()
	
	def validate_encoding(self, text):
		#re.sub('[\xe2]', '', text)
		text.translate(None, '\xe2')
			
	
	def to_html_file(self, filepath):
		f = open(filepath, 'w')
		html = self.to_html()
		f.write(html)
		f.close()
		

class FileDocument(object):
	"""This class represents a document of a single file in
	the project"""
	userinfo = {}
	def __init__(self, path):
		self.path = path #path to file associated with document
		self.get_user_info()
		self.get_file_stats()
	
	def get_user_info(self):
		"""Get user info about this file from the filesystem"""
		for ui in pwd.getpwall():
			self.userinfo[ui[2]] = ui
			
	def get_file_stats(self):
		"""get file stats about this file from the filesystem"""
		stats = os.stat(self.path)
		user = self.userinfo[stats.st_uid]
		#self.username = user.pw_name
		self.username = user.pw_gecos[:-3]
		self.modifytime = datetime.date.fromtimestamp(stats.st_mtime)
		
	def to_html(self):
		"""Convert file document to html"""
		source_dir = get_source_directory()
		css_path = source_dir + "printing.css"
		cmd = "source-highlight -n --style-css-file {0} --tab 2 -f html -i {1}".format(css_path, self.path)
		p = Popen(cmd.split(), shell=False, stdout=PIPE)

		file_path_name = os.path.relpath(self.path, get_current_directory())		
		html_string = """<h1>File: {0}</h1>
		<h3>Created By: {1}, Date: {2}</h3>
		""".format(file_path_name,
					self.username,
					str(self.modifytime))
		for line in p.stdout:
			html_string += line
		
		return html_string
		
	def to_latex(self):
		"""return string of latex"""
		pass
		
class Searcher(object):
	"""This class is used for searching the filsystem for
	the relevent files to include in the project"""
	code_extensions = ['c', 'h',
						'cpp', 'hpp',
						'cs',
						'go',
						'java',
						'py']

	def __init__(self, args):
		if args.extensions == None:
			self.extensions = self.code_extensions #auto extensions
		else:
			self.extensions = args.extensions
		
		self.build_re_extensions()
		
		self.re_exclusions = []
		if args.exclusions:
			self.exclusions = args.exclusions
			self.build_re_exclusions()
		
		if args.files == None:
			self.SEARCH_ARGS = False
		else:
			self.SEARCH_ARGS = True
			self.arg_filenames = args.files
		
		self.documents = []
		
		
	def build_re_extensions(self):
		"""Build regular expression for searching
		file extensions"""
		extensions_list = ""
		for ext in self.extensions:
			extensions_list += "{0}|".format(ext)
			
		extensions_list = extensions_list[:-1] #cut final bar
		re_string = ".*[.]({0})$".format(extensions_list)
		print(re_string)
		self.extension_re = re.compile(re_string)
		
	def build_re_exclusions(self):
		"""Build regular expression for excluding files"""
		for ex in self.exclusions:
			re_ex = re.compile(ex)
			self.re_exclusions.append(re_ex)
	
	def test_exclude(self, f):
		for re_ex in self.re_exclusions:
			if re_ex.match(f):
				return True
		
		return False
	
	def search(self):
		self.documents.append(ProjectDocument(get_current_directory()))
		if not self.SEARCH_ARGS:
			self.searchAuto()
		else:
			self.searchArgs()

	def searchAuto(self):
		current_dir = os.getcwd()
		for root, dirs, filenames in os.walk(current_dir):
			for f in filenames:
				fpath = os.path.join(root, f)
				#print(root + "/" + f)
				match = self.extension_re.match(f)
				if match:
					if self.test_exclude(fpath):
						print("excluded: {0}".format(fpath))
						continue
					self.documents[0].append(FileDocument(fpath))
	
	def searchArgs(self):
		for fname in self.arg_filenames:
			root = get_current_directory()
			#print(root, fname)
			path = os.path.join(root, fname)
			#print(path)
			self.documents[0].append(FileDocument(path))
		
	def handle_file_search(self, root, f):
		pass
        	
	
#extensions = extension_s.split(";")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Convert code to PDF files')
	parser.add_argument('--ext', metavar='Ext', type=str, dest='extensions', nargs='*',
		help='the letters of the file extensions')
	parser.add_argument('--exclude', metavar='Regex', type=str, dest='exclusions', nargs='*',
		help='each element of exclude is a regex to be excluded')
	parser.add_argument('-o', metavar='File', type=str, dest='outfile', nargs='?',
		help='name of output file')
	parser.add_argument('--user-name', type=str, dest='username', nargs='?',
		help='set custom user name')
	parser.add_argument('--project-name', type=str, dest='project_name', nargs='?',
		help='set custom project name')
	parser.add_argument('-i', metavar='File', type=str, dest='files', nargs='*',
		help='file names to be converted')

	args = parser.parse_args()
	outfile = args.outfile
	s = Searcher(args)
	s.search()
	doc = s.documents[0]
	
	if not outfile:
		outfile = "render.pdf"
	
	
	if outfile.split(".")[1] == "pdf":
		#doc.to_html_file("render.html")
		doc.to_pdf_file(outfile)
	else:
		doc.to_html_file(outfile)

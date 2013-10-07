Source2PDF
============

**Source2PDF** is a commandline tool, and python library used for the creation of 
syntax highlighted pdf documents containing software source code.

Source2PDF is currently capable of generating a single pdf document of an entire 
project by recursively scanning the project directory for relevant source files. 
It is also possible to instruct Source2PDF to exclude certain documents or folders 
using regular expressions.

Here is an example of the output you can expect: [Source2PDF.pdf](https://github.com/kellpossible/Source2PDF/blob/master/Source2Pdf.pdf?raw=true)

For information about the license, check [Source2PDF.py](https://github.com/kellpossible/Source2PDF/blob/master/Source2Pdf.py)

Installation
--------------

Uses python 2.7x
Required packages python libaries which can be installed
using [easy_install](https://pypi.python.org/pypi/setuptools) (as part of the 
setuptools collection):

        pisa, reportlab, html5lib and pygments

I've found the easiest way to get "easy\_install" on linux is by installing 
python2-setuptools or python-setuptools (depending on which one is for python2)
package using your system's package manager.

I have not tested this on windows yet, but it should work, so long as you can install these libraries.

Usage
--------------
Command line usage:

        usage: Source2Pdf.py [-h] [-e [Ext [Ext ...]]] [-x [Regex [Regex ...]]]
            [-o [File]] [-u [USERNAME]] [-n [PROJECT_NAME]]
            [--style [{monokai,manni,rrt,perldoc,borland,colorful,default,murphy,vs,trac,tango,fruity,autumn,bw,emacs,vim,pastie,friendly,native}]]
            [-l] [-i [File [File ...]]]

            Convert code to PDF files

            optional arguments:
              -h, --help            show this help message and exit
              -e [Ext [Ext ...]], --ext [Ext [Ext ...]]
                                    the letters of the file extensions
              -x [Regex [Regex ...]], --exclude [Regex [Regex ...]]
                                    each element of exclude is a regex to be excluded
              -o [File]             name of output file
              -u [USERNAME], --user-name [USERNAME]
                                    set custom user name
              -n [PROJECT_NAME], --project-name [PROJECT_NAME]
                                    set custom project name
              --style [{monokai,manni,rrt,perldoc,borland,colorful,default,murphy,vs,trac,tango,fruity,autumn,bw,emacs,vim,pastie,friendly,native}]
                                    set pygments style
              -l, --line-numbers    use line numbers
              -i [File [File ...]]  file names to be converted

Make sure to check out [build_pdf.sh](https://github.com/kellpossible/Source2PDF/blob/master/build_pdf.sh) as an example of usage

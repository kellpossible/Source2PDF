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
using pip. I have pip for python 2.7x aliased to *pip2* on my system.

        $ pip2 install -r requirements.txt

I have not tested this software on windows yet, but it should work provided you can get the dependencies installed.

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

Future Work
------------

I'm considering implementing the following functionality:
* binary exe package and installer for windows
* gui using python-pyside or wxpython
* index page, possibly with links to other sections in the pdf
* web application using [web2py](http://web2py.com/)

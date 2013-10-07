#!/bin/sh
python2 Source2Pdf.py --ext py sh --exclude .*AssemblyInfo.* .*gtk-gui.* \
-o Source2Pdf.pdf --project-name Source2Pdf --style default \
--line-numbers

#!/bin/sh
python2 Source2Pdf.py --ext py sh --exclude .*AssemblyInfo.* .*gtk-gui.* \
-o Source2Pdf.pdf --user-name "Luke Frisken" --project-name Source2Pdf

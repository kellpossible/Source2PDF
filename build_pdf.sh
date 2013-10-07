#!/bin/sh
#currently hidden folders with fullstop prefix are automatically excluded
#anyway, but this is just an example of how you might exclude it using regex
python2 Source2Pdf.py --ext py sh css --exclude .*[\\.]git.* \
-o Source2Pdf.pdf --project-name Source2Pdf --style default --user-name kellpossible \
--line-numbers

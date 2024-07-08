#! /usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip() # remove leading and trailing whitespaces /T /N /R
    words = line.split() # Découper la ligne en mots
    for word in words:
        print('%s\t%s' % (word, 1))

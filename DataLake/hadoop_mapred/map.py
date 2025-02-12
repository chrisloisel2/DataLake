#! /usr/bin/env python

import sys

for line in sys.stdin: # Pour chaque ligne de l'entrée standard
    line = line.strip() # On enlève les espaces en début et fin de ligne
    words = line.split() # On découpe la ligne en mots
    for word in words: # Pour chaque mot
        print('%s\t%s' % (word, 1)) # On affiche le mot et le nombre 1 séparés par une tabulation

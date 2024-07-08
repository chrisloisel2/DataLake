#! /usr/bin/env python

import sys

for line in sys.stdin:
    word, count = line.strip().split('\t')
    count = int(count)
    if word == current_word:
        current_count += count
    else:
        if current_word:
            print('%s\t%s' % (current_word, current_count))
        current_word = word
        current_count = count

if current_word:
    print('%s\t%s' % (current_word, current_count))

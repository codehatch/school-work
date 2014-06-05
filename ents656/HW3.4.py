#!/usr/bin/python

import sys
sys.path.append('.')

import word_mainip as wm

separated = wm.sep_words("Hello, world! How are you? Your ocenas are pretty. Incomplete sentence")
print(separated)
combined = wm.comb_words(separated)
print combined

print("")
print(separated[0])
print(wm.rev_word(separated[0]))
print(wm.rot13_word(separated[0]))
print(wm.anagram_word(separated[0]))
print(separated[0])
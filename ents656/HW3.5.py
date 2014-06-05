#!/usr/bin/python

import sys
sys.path.append('.')

import word_mainip as wm

# Read file into string
data = ""
with open("HW3-paragraph.txt") as myfile:
    data="".join(line.rstrip() for line in myfile)

# Strip leading/trailing whitespace
data = data.strip()

sentence_lists = wm.sep_words(data)
mod_words_list = []
first = True
for sentence in sentence_lists:

	rot13ed = wm.rot13_word(sentence)
	
	if first:
		mod_words_list.append(wm.anagram_word(rot13ed, 1029384756))
		first = False
	else:
		mod_words_list.append(wm.anagram_word(rot13ed))

# Recounstruct sentences
mod_paragraph = wm.comb_words(mod_words_list)

# Print to file with no more than 60 charactes per line
outfile=open('./out', 'w+')
while True:
	if (len(mod_paragraph) >= 60):
		# Find last space within 60 characters
		last_space = mod_paragraph[0:60].rfind(' ')

		# Print line with '\n'
		outfile.write(mod_paragraph[0:last_space] + "\n")

		# note last_space + 1 to skip over it
		mod_paragraph = mod_paragraph[last_space+1:]
	else:
		outfile.write(mod_paragraph+"\n")
		break

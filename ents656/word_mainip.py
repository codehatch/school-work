#!/usr/bin/python

import re
from string import maketrans
import random

def sep_words(line):
	words = []

	for chunk in re.findall(r'[^\?\.\!]*[\?\.\!]|[^\?\.\!]+', line):

		# Split on spaces and special characters
		chunks = re.split(r'\s|([\?\!\.])', chunk.strip())

		# Remove empty entries
		words.append(filter(None, chunks))

	# Remove empty
	words = filter(None, words)

	return words


def comb_words(words):
	terminators = ['.', '!', '?']
	output = ""
	for chunk in words:
		for word in chunk:
			if word not in terminators:
				output += " "
			output += word

	return output

def rev_word(words):
	rev = []

	for word in words:
		rev.append(word[::-1])
	return rev

def rot13_word(words):
	rot13 = []

	intab =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	outtab = "nopqrstuvwxzyabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
	trantab = maketrans(intab, outtab)

	for word in words:
		rot13.append(word.translate(trantab))

	return rot13


def anagram_word(words, seed=None):
	anagram = []

	terminators = ['.', '!', '?']

	# Seed random generate if given
	if seed is not None:
		random.seed(seed)

	for word in words:
		if word not in terminators:
			l = list(word)
			random.shuffle(l)
			anagram.append(''.join(l))
		else:
			anagram.append(word)

	return anagram

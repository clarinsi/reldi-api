# -*- coding: utf-8 -*-
import os
import sys
# sys.path.append('./lib')
from tokenizer import generate_tokenizer,tokenize,sentence_split,sentence_split_nonstd,spaces_re

class Segmenter(object,):
	'''Class segmenter'''

	def __init__(self, lang):
		self.lang = lang
		self.tokenizer = generate_tokenizer(lang)

	def segment(self, sentence):
		return sentence_split(tokenize (self.tokenizer, u'' + sentence), self.lang)

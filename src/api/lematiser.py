# -*- coding: utf-8 -*-
import os
import sys
import pycrfsuite 
import cPickle as pickle
from train_tagger import extract_features_msd

from segmenter import Segmenter

class Lematiser(object):
	'''Class segmenter'''

	def __init__(self, dc, lang):
		self.dc = dc
		self.lang = lang
		self.lemmatiser = {
			'model': pickle.load(open('assets/' + lang + '.lexicon.guesser')),
			'lexicon': pickle.load(open('assets/' + lang + '.lexicon'))
		}
	
	def getLemma(self, token, msd):
		lexicon = self.lemmatiser['lexicon']
		key = token.lower()+'_'+msd
		if key in lexicon:
			return lexicon[key][0].decode('utf8')
		if msd[:2]!='Np':
			for i in range(len(msd)):
				for key in lexicon.keys(key[:-(i+1)]):
					return lexicon[key][0].decode('utf8')
	
		return self.guessLemma(token, msd)

	def guessLemma(self, token, msd):
		model = self.lemmatiser['model']
		if msd not in model:
			return token
		else:
			return apply_rule(token, model[msd].predict(extract_features_lemma(token))[0], msd)

	def lematise(self, sentence, vert=False):
		tagger = self.dc.getInstance('tagger.' + self.lang)
		return [[(a,c) for a,b,c in sent] for sent in tagger.tagLematise(sentence, vert)]
		
	

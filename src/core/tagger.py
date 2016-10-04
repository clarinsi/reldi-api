# -*- coding: utf-8 -*-
import os
import sys
import pycrfsuite 
import cPickle as pickle
from train_tagger import extract_features_msd

from tokenizer import spaces_re

class Tagger(object,):
    '''Class tagger'''

    def __init__(self, lang, segmenter):
        self.lang = lang
        self.model = pycrfsuite.Tagger()
        self.model.open('assets/' + lang + '.msd.model')
        self.marisaTrie = pickle.load(open('assets/' + lang + '.marisa'))
        self.segmenter = segmenter

    def tag(self, sentence, vert=False):
        """Tags a sentence and returns tagged tokens"""
        output=[]
        if not vert:
            sentence = self.segmenter.segment(sentence)

        for sent in sentence:
            sent = [(e[0], e[1] + 1, e[2]) for e in sent if spaces_re.search(e[0]) == None]
            tokens = [e[0] for e in sent]
            output.append([(a, b) for a, b in zip(sent, self.model.tag(extract_features_msd(tokens, self.marisaTrie)))])
        return output


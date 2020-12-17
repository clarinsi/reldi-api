# -*- coding: utf-8 -*-
import os
import sys
import kenlm
import cPickle as pickle
from redi import redi
from tokenizer import spaces_re

class DiacriticRestorer(object,):
    '''Class segmenter'''

    def __init__(self, lang, segmenter):
        self.lang = lang
        self.tm=pickle.load(open('assets/wikitweetweb.'+lang+'.tm'))
        cnf=kenlm.Config()
        cnf.load_method=0
        self.lm=kenlm.LanguageModel('assets/wikitweetweb.'+lang+'.bin',cnf)
        self.segmenter = segmenter

    def restore(self, sentence, vert=False):
        output=[]
        if not vert:
            sentence = self.segmenter.segment(sentence)
        for sent in sentence:
            sent = [(e[0], e[1] + 1, e[2], e[3], e[4]) for e in sent if spaces_re.search(e[0]) == None]
            tokens = [e[0] for e in sent]
            output.append([(a, b) for a, b in zip(sent, redi(tokens,self.tm,self.lm))])
        return output


#!/usr/bin/python
# -*-coding:utf8-*-

from src.helpers import config

import os

reldir = os.path.dirname(os.path.abspath(__file__))
from tokenizer import spaces_re
from csmtiser import Csmtiser as CSMT

class Csmtiser(object):
    '''Class cSMTiser'''

    def __init__(self, lang, segmenter):
        self.lang = lang
        self.csmtiser =  CSMT(config['csmtiser'])
        self.segmenter = segmenter

    def tag(self, sentence, vert=False):
        """Tags a sentence and returns tagged tokens"""
        output=[]
        if not vert:
            sentence = self.segmenter.segment(sentence)

        tokens = [e[0] for sent in sentence for e in sent]
        token_to_normalized_token = self.csmtiser.normalise_tokens(tokens)

        for sent in sentence:
            sent = [(e[0], e[1] + 1, e[2]) for e in sent if spaces_re.search(e[0]) == None]
            tokens = [[(token_to_normalized_token[t],s,e)] for t,s,e in sent]
            output.append(tokens)
        return output



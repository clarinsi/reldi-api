# -*- coding: utf-8 -*-
import os
import sys
import pycrfsuite 
import cPickle as pickle
from train_tagger import extract_features_msd

from tokenizer import spaces_re

class Tagger(object,):
    '''Class segmenter'''

    def __init__(self, dc, lang):
        self.dc = dc
        self.lang = lang
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open('assets/' + lang + '.msd.model')
        self.trie = pickle.load(open('assets/' + lang + '.marisa'))

    def tag(self, sentence, vert=False):
        output=[]
        if not vert:
            segmenter = self.dc.getInstance('segmenter.' + self.lang)
            sentence = segmenter.segment(sentence)

        for sent in sentence:
            sent = [(e[0], e[1], e[2]) for e in sent if spaces_re.search(e[0]) == None]
            tokens = [e[0] for e in sent]
            output.append([(a, b) for a, b in zip(sent, self.tagger.tag(extract_features_msd(tokens, self.trie)))])
        return output

    def tagLematise(self, sentence, vert=False):
        lematiser = self.dc.getInstance('lematiser.' + self.lang)
        segmenter = self.dc.getInstance('segmenter.' + self.lang)
        output=[]
        if not vert:
            sentence = segmenter.segment(sentence)
        for sent in sentence:
            sent = [(e[0], e[1], e[2]) for e in sent if spaces_re.search(e[0]) == None]
            tokens = [e[0] for e in sent]
            outputtag=[(a,b) for a,b in zip(sent, self.tagger.tag(extract_features_msd(tokens, self.trie)))]
            tag=[e[1] for e in outputtag]
            output.append([(a,b,lematiser.getLemma(a[0],b)) for a,b in zip(sent,tag)])
        return output


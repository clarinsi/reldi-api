#!/usr/bin/python
# -*-coding:utf8-*-

import warnings
from itertools import izip

warnings.filterwarnings("ignore")

import sys
import os

reldir = os.path.dirname(os.path.abspath(__file__))

from train_ner_tagger import extract_features
from subprocess import Popen, PIPE
import cPickle as pickle
from StringIO import StringIO
import pycrfsuite


class NerTagger(object):
    '''Class segmenter'''

    def __init__(self, lang, tagger):
        self.tagger = tagger
        self.lang = lang
        self.ner_tagger = pycrfsuite.Tagger()
        # self.ner_tagger.open(os.path.join(reldir, lang + '.ner.model'))
        self.ner_tagger.open('assets/' + lang + '.ner.model')

        self._brown = dict(
            [(e[1].decode('utf8'), e[0]) for e in [e.split('\t') for e in open('assets/' + lang + '.brown')]])

    def tag_sent(self, tokens, tags):
        # print extract_features(tokens,tags,brown)
        return self.ner_tagger.tag(extract_features(tokens, tags, self._brown))

    def tag(self, text):
        tagged_sents = self.tagger.tag(text)

        ner_tagged_sents=[]
        for sent in tagged_sents:
            tokens = [e[0][0] for e in sent]
            tags = [e[1] for e in sent]

            ners = self.tag_sent(tokens,tags)
            ner_tagged_sents.append([(a[0], a[1], b) for a,b in izip(sent,ners)]) # append ners to the result tuples

        return ner_tagged_sents







            # for sent in sentence:
            #     sent = [(e[0], e[1] + 1, e[2]) for e in sent if spaces_re.search(e[0]) == None]
            #     tokens = [e[0] for e in sent]
            #     output.append([(a, b) for a, b in zip(sent, self.model.tag(extract_features_msd(tokens, self.marisaTrie)))])
            # return 0 # output

    def read_and_write(self, istream, index, msdindex, ostream):
        entry_list = []

        for line in istream:
            if line.strip() == '':
                tokens = []
                tags = []
                for token, tag in [(e[index], e[msdindex]) for e in entry_list]:
                    if ' ' in token:
                        if len(token) > 1:
                            tokens.extend(token.split(' '))
                            tags.extend(tag.split(' '))
                    else:
                        tokens.append(token)
                        tags.append(tag)
                tag_counter = 0
                ner = self.tag_sent(tokens, tags)
                ner_proper = []
                for token in [e[index] for e in entry_list]:
                    if ' ' in token:
                        if len(token) == 1:
                            ner_proper.append(' ')
                        else:
                            ner_proper.append(' '.join(ner[tag_counter:tag_counter + token.count(' ') + 1]))
                            tag_counter += token.count(' ') + 1
                    else:
                        ner_proper.append(ner[tag_counter])
                        tag_counter += 1
                ostream.write(u''.join(
                    ['\t'.join(entry) + '\t' + tag + '\n' for entry, tag in zip(entry_list, ner_proper)]) + '\n')
                entry_list = []
            else:
                entry_list.append(line[:-1].decode('utf8').split('\t'))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='NER tagger for Slovene (Croatian and Serbian to follow)')
    parser.add_argument('lang', help='language of the text', choices=['sl', 'sl.true', 'sl.lower'])
    parser.add_argument('-i', '--index', help='index of the column containing surface forms', type=int, default=1)
    parser.add_argument('-m', '--msdindex', help='index of the column containing MSDs', type=int, default=2)
    args = parser.parse_args()
    tagger = NerTagger(args.lang)
    tagger.read_and_write(sys.stdin, args.index - 1, args.msdindex - 1, sys.stdout)

# -*- coding: utf-8 -*-
import os

import requests
import urllib
from subprocess import Popen, PIPE, STDOUT
import sys, traceback

class DependencyParser(object):
    '''Class segmenter'''

    def __init__(self, lang, lemmatiser):
        self.lang = lang
        self.lemmatiser = lemmatiser



    def _makeRequest(self, text):
        result = requests.post("http://localhost:9090/parse",
                      data={'lang': self.lang.lower(), 'text': text})

        return result.text

    def parse(self, text):

        sentences = self.lemmatiser.tagLemmatise(text)

        result = []
        parsedSentences = []
        # Feed data
        for sentence in sentences:
            parsedSentence = []
            inputString = ""
            for tokenIdx, token in enumerate(sentence):
                inputString += "{0}	{1}	{2}	_	{3}	_	{4}	_	_	_	_	_	_\n" \
                    .format(tokenIdx + 1, token[0][0], token[2], token[1][0], token[1])
            inputString += "\n"
            text = self._makeRequest(inputString)

            # split all the sentences by New Line and removed the empty spaces or empty lines
            content = map(lambda x: x.split("\t"), text.split('\n'))
            print content
            for tokenIdx, token in enumerate(sentence):
                parsedSentence.append((token[0], token[1], token[2], (content[tokenIdx][9], content[tokenIdx][11])))

            parsedSentences.append(parsedSentence)

            # for token in sentence:
                # for line in content:
                #     parts = line.split('\t')
                #     parsedSentence.append((token[0], token[1], token[2], (parts[9], parts[11])))

            # result.append(parsedSentence)

        #     self.parser.stdin.write(inputString)
        #
        #     # Read data
        #     for token in sentence:
        #         parsedToken = self.parser.stdout.readline().rstrip()                          #reads first line of the result
        #         parts = parsedToken.split('\t')                                               #splits line by TABS
        #         parsedSentence.append((token[0], token[1], token[2], (parts[9], parts[11])))  #appends elements to a parsed sentences
        #
        #     result.append(parsedSentence)
        #
        #     # Read blank
        #     self.parser.stdout.readline().rstrip()


        return parsedSentences



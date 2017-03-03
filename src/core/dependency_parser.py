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
                      data={'lang': self.lang.lower(), 'text': urllib.quote(text)})

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
            for tokenIdx, token in enumerate(sentence):
                parsedSentence.append((token[0], token[1], token[2], (content[tokenIdx][9], content[tokenIdx][11])))

            parsedSentences.append(parsedSentence)


        return parsedSentences



# -*- coding: utf-8 -*-

import requests
import urllib

class DependencyParser(object):
    '''Class segmenter'''

    def __init__(self, lang, lemmatiser):
        self.lang = lang
        self.lemmatiser = lemmatiser



    def _makeRequest(self, text):
        result = requests.post("http://localhost:9090/parse",
                      data={'lang': self.lang.lower(), 'text': urllib.quote(text)},
                      timeout=1000)

        return result.text

    def parse(self, text):

        sentences = self.lemmatiser.tagLemmatise(text)
        payloadString = ""
        # Feed data
        for sentence in sentences:
            for tokenIdx, token in enumerate(sentence):
                payloadString += "{0}	{1}	{2}	_	{3}	_	{4}	_	_	_	_	_	_\n" \
                    .format(tokenIdx + 1, token[0][0], token[2], token[1][0], token[1])
            payloadString += "\n"

        print "Make request"
        parsedText = self._makeRequest(payloadString)
        print "Done"
        parsedTextSentences = parsedText.split("\n\n")

        parsedSentences = []
        # split all the sentences by New Line and removed the empty spaces or empty lines
        for sidx, sentence in enumerate(sentences):
            parsedSentence = []
            content = map(lambda x: x.split("\t"), parsedTextSentences[sidx].split('\n'))
            for tokenIdx, token in enumerate(sentence):
                parsedSentence.append((token[0], token[1], token[2], (content[tokenIdx][9], content[tokenIdx][11])))

            parsedSentences.append(parsedSentence)


        return parsedSentences



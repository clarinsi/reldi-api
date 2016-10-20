# -*- coding: utf-8 -*-
import os

from subprocess import Popen, PIPE, STDOUT


class DependencyParser(object):
    '''Class segmenter'''

    def __init__(self, lang, lemmatiser):
        self.lang = lang
        self.lemmatiser = lemmatiser
        self._read_initial_output = False

        jarFile = os.path.realpath("bin/anna-3.5-custom-build.jar")
        parserModelFile = os.path.realpath("assets/set.hr.conll.MODEL")

        self.parser = Popen(["java", "-cp", jarFile, "is2.parser.Parser", "-model", parserModelFile], stdout=PIPE,
                            stdin=PIPE, stderr=PIPE)

        # read initial data
        self.parser.stdout.readline()
        self.parser.stdout.readline()
        self.parser.stdout.readline()
        self.parser.stdout.readline()
        self.parser.stdout.readline()

    def parse(self, text):

        sentences = self.lemmatiser.tagLemmatise(text)
        result = []

        # Feed data
        for sentence in sentences:
            parsedSentence = []
            inputString = ""
            for tokenIdx, token in enumerate(sentence):
                inputString += "{0}	{1}	{2}	_	{3}	_	{4}	_	_	_	_	_	_\n" \
                    .format(tokenIdx + 1, token[0][0], token[2], token[1][0], token[1])

            inputString += "\n"
            self.parser.stdin.write(inputString)

            # Read data
            for token in sentence:
                parsedToken = self.parser.stdout.readline().rstrip()
                parts = parsedToken.split('\t')
                parsedSentence.append((token[0], token[1], token[2], (parts[9], parts[11])))

            result.append(parsedSentence)

            # Read blank
            self.parser.stdout.readline().rstrip()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.parser.kill()

    def dispose(self):
        self.parser.kill()


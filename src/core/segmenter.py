# -*- coding: utf-8 -*-
import re
# sys.path.append('./lib')
from tokenizer import generate_tokenizer, tokenize, sentence_split, sentence_split_nonstd, spaces_re


class Segmenter(object, ):
    '''Class segmenter'''

    def __init__(self, lang):
        self.lang = lang
        self.tokenizer = generate_tokenizer(lang)

    def segment(self, sentence,non_standard_sentence_split=False):
        """
        Segments a sentence into tokens
        """

        lines = filter(lambda x: x.strip() != '', sentence.replace('\xef\xbb\xbf', '').splitlines())
        result = []
        for cntp, line in enumerate(lines):
            ssplitter=sentence_split_nonstd if non_standard_sentence_split else sentence_split

            tokens = ssplitter(tokenize(self.tokenizer, unicode(line)), self.lang)

            enriched_tokens = []
            for cnts, sentence in enumerate(tokens):
                enriched_tokens.append([(token[0], token[1], token[2], str(cntp+1), str(cnts+1))
                                        for token in sentence])

            result.extend(enriched_tokens)

        return result




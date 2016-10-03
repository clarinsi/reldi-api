# -*- coding: utf-8 -*-
import time
import sys
import os

sys.path.append(os.path.realpath('src/db'))
from ..db.query_expression import QueryExpression
from ..db.lexicon_db import LexiconDB


def isRegex(s):
    regexChars = ['[', ']', '-', '*', '+', '(', ')', '^', '$', '+']


# Main lexicon class
class Lexicon(object, ):
    '''Class lexicon'''

    def __init__(self, lang):
        if lang is None:
            raise ValueError("Language not set")

        self.language = lang

    def query_entry(self, surface=None, lemma=None, msd=None, rhymes_with=None, no_of_syllables=None,
                    surface_is_regexp=False, msd_is_regex=False, lemma_is_regex=False):

        """
        Queries the lexicon for entries that match the input parameters
        """

        # Instantiate a query expression
        expr = QueryExpression()

        # Select from table lexicon_{language}
        expr.select(['surface', 'tags', 'lemma']).fromTable('lexicon')

        # Set surface
        if surface_is_regexp and surface is not None:
            expr.where('surface', 'REGEXP', surface)
        elif surface is not None:
            if '%' in surface:
                expr.where('surface', 'like', surface)
            else:
                expr.where('surface', '=', surface)

        # Set lemma
        if lemma_is_regex and lemma is not None:
            expr.where('lemma', 'REGEXP', lemma)
        elif lemma is not None:
            if '%' in lemma:
                expr.where('lemma', 'LIKE', lemma)
            else:
                expr.where('lemma', '=', lemma)

        # Set tags
        if msd_is_regex and msd is not None:
            expr.where('lemma', 'REGEXP', lemma)
        elif msd is not None:
            if '%' in msd:
                expr.where('tags', 'like', msd)
            else:
                expr.where('tags', '=', msd)

        # Set number of syllables
        if no_of_syllables is not None:
            expr.where('no_of_syllables', '=', int(no_of_syllables) + 1)

        # Set number of syllables
        if rhymes_with is not None:
            expr.where('last_syllable', '=', rhymes_with)

        db = LexiconDB.getInstance(self.language)
        sql = expr.toSQL()

        result = db.query(sql)
        resultMap = map(lambda x: (
            x[0].encode('utf-8'),
            x[1].encode('utf-8'),
            x[2].encode('utf-8')
        ), result)

        return resultMap

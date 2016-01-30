# -*- coding: utf-8 -*-
import time
from query_expression import QueryExpression
from reldi_db import LexiconDB

def isRegex(s):
	regexChars = ['[', ']', '-', '*', '+', '(', ')', '^', '$', '+']

# Main lexicon class
class Lexicon(object,):
	'''Class lexicon'''

	def __init__(self, lang):
		if lang is None:
			raise ValueError("Language not set")

		self.language = lang

	def query_entry(self, surface = None, lemma = None, msd = None, rhymes_with = None, no_of_syllables = None):
		"""Queries the lexicon for entries that match the input parameters

			Parameters:
			surface - surface from
			lemma - lemma
			msd - descriptor tags
			rhymes_wyth - rhymes with word
			no_of_syllables - number of syllabels

		"""

		# Instantiate a query expression
		expr = QueryExpression()

		# Select from table lexicon_{language}
		expr.select(['surface', 'tags', 'lemma']).fromTable('lexicon')

		# Set surface
		if surface is not None and '%' in surface:
			expr.where('surface', 'like', surface)
		elif surface is not None:
			expr.where('surface', '=', surface)

		# Set lemma
		if lemma is not None and '%' in lemma:
			expr.where('lemma', 'like', lemma)
		elif lemma is not None:
			expr.where('lemma', '=', lemma)
		
		# Set tags
		if msd is not None and '%' in msd:
			expr.where('tags', 'like', msd)
		elif msd is not None:
			expr.where('tags', '=', msd)

		# Set number of syllables
		if no_of_syllables is not None:
			expr.where('no_of_syllables', '=', no_of_syllables)

		db = LexiconDB(self.language)
		sql = expr.toSQL()
		result = db.query(sql)
		resultMap = map(lambda x: (
			x[0].encode('utf-8'),
			x[1].encode('utf-8'),
			x[2].encode('utf-8')	
		), result)

		return resultMap


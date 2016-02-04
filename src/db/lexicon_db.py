# -*- coding: utf-8 -*-
import os
import sqlite3
import re

from reldi_db import DB

class LexiconDB(DB):
	# Object constructor
	def __init__(self, language):
		'''Override database'''
		thispath = os.path.dirname(os.path.realpath(__file__))
		database = os.path.realpath('assets/') + '/lexdb_' + language
		DB.__init__(self, database)

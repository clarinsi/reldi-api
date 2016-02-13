# -*- coding: utf-8 -*-
import os
import sqlite3
import re

from reldi_db import DB

class LexiconDB(DB):
    
    _instance = None

    @staticmethod
    def getInstance(language):
        database = os.path.realpath('assets/') + '/lexdb_' + language

        if (LexiconDB._instance is None):
            LexiconDB._instance = LexiconDB(DB._THE_MAGIC_WORD)
            if (LexiconDB._instance._connection is None):
                # Initialize connection
                LexiconDB._instance._connection = sqlite3.connect(database, isolation_level=None)
                LexiconDB._instance._connection.text_factory = str
                LexiconDB._instance._client = LexiconDB._instance._connection.cursor()
            
        return LexiconDB._instance
# -*- coding: utf-8 -*-
import os
import sqlite3
import re

from reldi_db import DB


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


class LexiconDB(DB):
    _instances = {
        'hr': None,
        'sr': None,
        'sl': None
    }

    @staticmethod
    def getInstance(language):
        database = os.path.realpath('assets/') + '/lexdb_' + language

        if LexiconDB._instances[language] is None:
            LexiconDB._instances[language] = LexiconDB(DB._THE_MAGIC_WORD)
            if LexiconDB._instances[language]._connection is None:
                # Initialize connection
                LexiconDB._instances[language]._connection = sqlite3.connect(database, isolation_level=None)
                LexiconDB._instances[language]._connection.text_factory = str
                LexiconDB._instances[language]._client = LexiconDB._instances[language]._connection.cursor()
                LexiconDB._instances[language]._connection.create_function("REGEXP", 2, regexp)

        return LexiconDB._instances[language]

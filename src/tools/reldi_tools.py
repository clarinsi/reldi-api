#!/usr/bin/env python
# -*- coding: utf-8 -*-

from import_lexicon import ImportLexiconCommand
from query_lexicon import QueryLexiconCommand

from cleo import Application

application = Application()
application.add(ImportLexiconCommand())
application.add(QueryLexiconCommand())

if __name__ == '__main__':
    application.run()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from import_lexicon import ImportLexiconCommand
from query_lexicon import QueryLexiconCommand
from create_user import CreateUserCommand
from create_user import LoginUserCommand

from cleo import Application

application = Application()
application.add(ImportLexiconCommand())
application.add(QueryLexiconCommand())
application.add(CreateUserCommand())
application.add(LoginUserCommand())

if __name__ == '__main__':
    application.run()
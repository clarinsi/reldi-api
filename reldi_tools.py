#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleo import Application

from tools.dbtools.reset_db import ResetDB
from tools.lextools.import_lexicon import ImportLexiconCommand
from tools.lextools.query_lexicon import QueryLexiconCommand
from tools.usertools.create_user import CreateUserCommand
from tools.usertools.delete_user import DeleteUserByUsernameCommand
from tools.usertools.get_user import GetUserByUsernameCommand
from tools.usertools.login_user import LoginUserWithCredentials

application = Application()
application.add(ImportLexiconCommand())
application.add(QueryLexiconCommand())
application.add(CreateUserCommand())
application.add(GetUserByUsernameCommand())
application.add(DeleteUserByUsernameCommand())
application.add(LoginUserWithCredentials())
application.add(ResetDB())

if __name__ == '__main__':
    application.run()
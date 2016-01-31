#!/usr/bin/env python
# -*- coding: utf-8 -*-

from import_lexicon import ImportLexiconCommand
from query_lexicon import QueryLexiconCommand
from usertools.get_user import GetUserByUsernameCommand
from usertools.create_user import CreateUserCommand
from usertools.delete_user import DeleteUserByUsernameCommand
from usertools.login_user import LoginUserWithCredentials
from dbtools.reset_db import ResetDB

from cleo import Application

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
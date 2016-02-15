#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleo import Application

from dbtools.reset_db import ResetDB
from lextools.import_lexicon import ImportLexiconCommand
from lextools.query_lexicon import QueryLexiconCommand
from usertools.create_user import CreateUserCommand
from usertools.delete_user import DeleteUserByUsernameCommand
from usertools.get_user import GetUserByUsernameCommand
from usertools.login_user import LoginUserWithCredentials

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
# -*- coding: utf-8 -*-
import sys
import os
import regex
import codecs

dbpath = os.path.realpath('../models')
sys.path.append(dbpath)

from cleo import Command, InputArgument, InputOption
from user_model import UserModel
from auth_token_model import AuthTokenModel


class GetUserByUsernameCommand(Command):

    name = 'user:get-by-username'

    description = 'Adds a user to the users table'

    arguments = [
        {
            'name': 'username',
            'description': 'Username',
            'required': True
        }
    ]

    def __init__(self):
        super(GetUserByUsernameCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        # Read parameters
        username = i.get_argument('username')
        user = UserModel.getByAttributeSingle('username', username)

        print "all user tokens:"
        tokens = user.getAllAuthTokens()
        for token in tokens:
            print token

        print "valid user tokens:"
        tokens = user.getValidAuthTokens()
        for token in tokens:
            print token








        


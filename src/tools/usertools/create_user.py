# -*- coding: utf-8 -*-
import sys
import os
import regex
import codecs

dbpath = os.path.realpath('../models')
sys.path.append(dbpath)

from cleo import Command, InputArgument, InputOption
from user_model import UserModel

class CreateUserCommand(Command):

    name = 'user:add'

    description = 'Adds a user to the users table'

    arguments = [
        {
            'name': 'username',
            'description': 'Username',
            'required': True
        },
        {
            'name': 'email',
            'description': 'Email',
            'required': True
        },
        {
            'name': 'password',
            'description': 'Password',
            'required': True
        },
        {
            'name': 'project',
            'description': 'Project',
            'required': True
        },
        {
            'name': 'requests_limit',
            'description': 'Requests limit per month',
            'required': True
        },
        {
            'name': 'role',
            'description': 'User role (admin or user)',
            'required': True
        }
    ]

    def __init__(self):
        super(CreateUserCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        # Read parameters
        user = UserModel()
        user.username = i.get_argument('username')
        user.password = i.get_argument('password')
        user.project = i.get_argument('project')
        user.requests_limit = i.get_argument('requests_limit')
        user.requests_made = 0
        user.status = 'active'
        user.role = i.get_argument('role')
        user.save()


class LoginUserCommand(Command):

    name = 'user:login'

    description = 'Adds a user to the users table'

    arguments = [
        {
            'name': 'username',
            'description': 'Username',
            'required': True
        },
        {
            'name': 'password',
            'description': 'Password',
            'required': True
        }
    ]

    def __init__(self):
        super(LoginUserCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        # Read parameters
        username = i.get_argument('username')
        password = i.get_argument('password')
        
        UserActiveRecord.getByUsernameAndPassword(username, password)
        





# -*- coding: utf-8 -*-
from cleo import Command, InputArgument, InputOption
from src.models.user_model import UserModel


class LoginUserWithCredentials(Command):

    name = 'user:login'

    description = 'Logs in a user'

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
        super(LoginUserWithCredentials, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        # Read parameters
        username = i.get_argument('username')
        password = i.get_argument('password')

        user = UserModel.getByAttributeSingle('username', username)
        user.save()
        token = user.generateToken(password)
        token.save()
        for token in user.getValidAuthTokens():
            print token




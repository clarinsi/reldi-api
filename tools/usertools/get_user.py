# -*- coding: utf-8 -*-
from cleo import Command, InputArgument, InputOption
from src.models.user_model import UserModel


class GetUserByUsernameCommand(Command):

    name = 'user:get'

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
        user = UserModel.getByUsername(username)
        print user







        


# -*- coding: utf-8 -*-

from cleo import Command, InputArgument, InputOption
from ...models.user_model import UserModel

class DeleteUserByUsernameCommand(Command):

    name = 'user:delete-by-username'

    description = 'Adds a user to the users table'

    arguments = [
        {
            'name': 'username',
            'description': 'Username',
            'required': True
        }
    ]

    def __init__(self):
        super(DeleteUserByUsernameCommand, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        # Read parameters
        user = UserModel.getByUsername(i.get_argument('username'))
        user.delete()

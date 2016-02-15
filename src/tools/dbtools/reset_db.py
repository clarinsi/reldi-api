# -*- coding: utf-8 -*-
from cleo import Command, InputArgument, InputOption

from ...db.users_db import UsersDB
from ...models.user_model import UserModel


class ResetDB(Command):

    name = 'db:reset'

    description = 'Resets the database'

    arguments = [

    ]

    def __init__(self):
        super(ResetDB, self).__init__()

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        
        UsersDB.getInstance().reset()
        
        user = UserModel()
        user.username = 'admin'
        user.email = 'admin@admin.com'
        user.setPassword('admin')
        user.role = 'admin'
        user.status = 'active'
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.save()

        user = UserModel()
        user.username = 'user'
        user.email = 'user@user.com'
        user.setPassword('user')
        user.role = 'user'
        user.status = 'active'
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.save()

        user = UserModel()
        user.username = 'pending'
        user.email = 'pending@pending.com'
        user.setPassword('user')
        user.role = 'user'
        user.status = 'pending'
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.save()

        user = UserModel()
        user.username = 'blocked'
        user.email = 'blocked@blocked.com'
        user.setPassword('user')
        user.role = 'user'
        user.status = 'blocked'
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.save()




        

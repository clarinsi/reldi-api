# -*- coding: utf-8 -*-
import sys
import os
import regex
import codecs

modelspath = os.path.realpath('../models')
dbpath = os.path.realpath('../db')
sys.path.append(modelspath)
sys.path.append(dbpath)

from cleo import Command, InputArgument, InputOption
from users_db import UsersDB
from user_model import UserModel

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
        user.setPassword('admin')
        user.role = 'admin'
        user.status = 'active'
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.save()




        

import sys, os

dbpath = os.path.realpath('../db')
dbpath = os.path.realpath('..')
dbpath = os.path.realpath('../models')

import re
from users_db import UsersDB
from model import Model
from query_expression import QueryExpression
<<<<<<< HEAD
from helpers import hash_password, verify_password, generate_token, get_unix_timestamp
=======
from helpers import hash_password, verify_password, generate_token, to_unix_timestamp
>>>>>>> c7ab339f33d7f110f0e4107afa1ddb7cf2abead9
from datetime import datetime, timedelta
import pytz


class AuthTokenModel(Model):

    SHORT_LASTING_TOKEN_HOURS_SPAN = 1
    
    @classmethod
    def model_props(cls):
        return ['user_id', 'token', 'expiration_timestamp', 'is_long_lasting']
    
    @classmethod
    def table_name(cls):
        return 'auth_tokens'

    @classmethod
    def primary_key(cls):
        return 'id'

    # Object constructor
    def __init__(self):
        '''Override database'''

        Model.__init__(self);

    def isValid(self):
        if self.expiration_timestamp is None:
            return True

        then = to_unix_timestamp(self.expiration_timestamp)
        now = to_unix_timestamp(datetime.now())

        return then > now

    def extend(self):
        self.expiration_timestamp = to_unix_timestamp(datetime.now() + AuthTokenModel.SHORT_LASTING_TOKEN_HOURS_SPAN)

    def toDbModel(self):
        dbModel = super(AuthTokenModel, self).toDbModel()
        dbModel['expiration_timestamp'] = to_unix_timestamp(dbModel['expiration_timestamp'])
        return dbModel

    @staticmethod
    def generate(is_long_lasting):
        token = AuthTokenModel()
        token.token = generate_token()
        token.is_long_lasting = is_long_lasting
        if (is_long_lasting):
            token.expiration_timestamp = None
        else:
            token.expiration_timestamp = datetime.now() + timedelta(hours = AuthTokenModel.SHORT_LASTING_TOKEN_HOURS_SPAN)
        return token


    @classmethod
    def fromDatabase(cls, row):
        model = super(AuthTokenModel, cls).fromDatabase(row)
        model.expiration_timestamp = datetime.fromtimestamp(float(model.expiration_timestamp))
        return model

import sys, os

dbpath = os.path.realpath('../db')
dbpath = os.path.realpath('..')
dbpath = os.path.realpath('../models')
sys.path.append(dbpath)
import re
from users_db import UsersDB
from model import Model
from query_expression import QueryExpression
from helpers import hash_password, verify_password, generate_token, get_unix_timestamp
from datetime import datetime, timedelta

class AuthTokenModel(Model):

    SHORT_LASTING_TOKEN_HOURS_SPAN = 1
    
    @classmethod
    def model_props(cls):
        return ['user_id', 'token', 'token_expiration_timestamp', 'is_long_lasting']
    
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
        if self.is_long_lasting:
            return True
        
        then = self.token_expiration_timestamp
        now = datetime.now()

        return then > now

    def toDbModel(self):
        dbModel = super(AuthTokenModel, self).toDbModel()
        dbModel['token_expiration_timestamp'] = get_unix_timestamp(dbModel['token_expiration_timestamp'])
        return dbModel

    @staticmethod
    def generate(is_long_lasting):
        token = AuthTokenModel()
        token.token = generate_token()
        token.is_long_lasting = is_long_lasting
        if (is_long_lasting):
            token.token_expiration_timestamp = None
        else:
            token.token_expiration_timestamp = datetime.now() + timedelta(hours = AuthTokenModel.SHORT_LASTING_TOKEN_HOURS_SPAN)
        return token


    @classmethod
    def fromDatabase(cls, row):
        model = super(AuthTokenModel, cls).fromDatabase(row)
        model.token_expiration_timestamp = datetime.fromtimestamp(float(model.token_expiration_timestamp))
        return model


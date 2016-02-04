import sys, os

dbpath = os.path.realpath('../db')
dbpath = os.path.realpath('..')
dbpath = os.path.realpath('../models')
sys.path.append(dbpath)
import re
import time
from users_db import UsersDB
from model import Model
from query_expression import QueryExpression
from helpers import hash_password, verify_password, generate_token
from datetime import datetime, timedelta

class AuthTokenModel(Model):

    SHORT_LASTING_TOKEN_HOURS_SPAN = 1
    
    @classmethod
    def model_props(cls):
        return ['user_id', 'token', 'token_expiration_timestamp']
    
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

    def isExpired(self):
        if (self.token_expiration_timestamp is None):
            return False

    def toDbModel(self):
        dbModel = super(AuthTokenModel, self).toDbModel()
        unixtime = time.mktime(dbModel['token_expiration_timestamp'].timetuple())
        dbModel['token_expiration_timestamp'] = unixtime
        return dbModel

    @staticmethod
    def getByUserId(user_id):
        db = UsersDB.getInstance()
        expression = QueryExpression()
        expression.fromTable('auth_tokens')
        expression.where('user_id', '=', user_id)
        result = db.query(expression.toSQL())

        if (len(result) == 0):
            return []

        return map(lambda x: AuthTokenModel.fromDatabase(x), result)

    @staticmethod
    def generate(is_long_lasting):
        token = AuthTokenModel()
        token.token = generate_token()
        token.is_long_lasting = is_long_lasting
        if (is_long_lasting):
            token.token_expiration_timestamp = None
        else:
            token.token_expiration_timestamp = datetime.now() + timedelta(hours = 1)
        return token


    @classmethod
    def fromDatabase(cls, row):
        model = super(AuthTokenModel, cls).fromDatabase(row)
        model.token_expiration_timestamp = datetime.fromtimestamp(float(model.token_expiration_timestamp))
        return model


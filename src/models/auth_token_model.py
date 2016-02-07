import sys, os

helperspath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.append(helperspath)

import re
from users_db import UsersDB
from model import Model
from query_expression import QueryExpression
from helpers import hash_password, verify_password, generate_token, to_unix_timestamp
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
        self.expiration_timestamp = to_unix_timestamp(datetime.now() + timedelta(hours = AuthTokenModel.SHORT_LASTING_TOKEN_HOURS_SPAN))

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


import sys, os

dbpath = os.path.realpath('../db')
dbpath = os.path.realpath('..')
dbpath = os.path.realpath('../models')
sys.path.append(dbpath)

from users_db import UsersDB
from model import Model
from query_expression import QueryExpression
from helpers import hash_password
from helpers import verify_password
from helpers import generate_token
from helpers import get_unix_timestamp
from auth_token_model import AuthTokenModel
from datetime import datetime, timedelta


class UserModel(Model):

    @classmethod
    def model_props(cls):
        return [
            'username', 'password', 'project', 'requests_limit', 
            'requests_made', 'last_request_datetime', 'role', 'status'
        ]
    
    @classmethod
    def table_name(cls):
        return 'users'

    @classmethod
    def primary_key(cls):
        return 'id'

    # Object constructor
    def __init__(self):
        self.tokens = []
        Model.__init__(self);


    def setPassword(self, password):
        self.password = hash_password(password)


    def generateToken(self, password, is_long_lasting = False):
        isPasswordValid = verify_password(password, self.password)
        if (not isPasswordValid):
            raise ValueError("Invaid password")
        token = AuthTokenModel.generate(is_long_lasting)
        token.user_id = self.id
        return token


    def getAllAuthTokens(self):
        tokens = AuthTokenModel.getByAttribute('user_id', self.id)
        return tokens


    def getValidAuthTokens(self):
        db = UsersDB.getInstance()
        sql = "SELECT * FROM {0} WHERE user_id = {1} AND (is_long_lasting = 1 OR token_expiration_timestamp > {2})"
        expiration_timestamp = datetime.now()
        sql = sql.format(AuthTokenModel.table_name(), self.id, get_unix_timestamp(expiration_timestamp))
        result = db.query(sql)

        if (len(result) == 0):
            return []

        return map(lambda x: AuthTokenModel.fromDatabase(x), result)


    def validateToken(self, token):
        token = AuthTokenModel.getByAttributesSingle(['token', 'user_id'], [token, self.id]);
        if token is None:
            return False

        return token.isValid()



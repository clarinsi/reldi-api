import sys, os

dbpath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../db')
sys.path.append(dbpath)

helperspath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.append(helperspath)

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
        self.token = None
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

    def loadToken(self, token):
        self.token = AuthTokenModel.getByAttributesSingle(['user_id', 'token'], [self.id, token])

    def isAuthorized(self):
        return self.token is not None and token.isValid()

    def getAuthTokens(self):
        tokens = AuthTokenModel.getByUserId(self.id)
        return tokens

    def block(self):
        self.status = 'blocked'

    def activate(self):
        self.status = 'active'

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

    # TODO: extendTokenExpiraionDate


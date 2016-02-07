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
from auth_token_model import AuthTokenModel

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

    @staticmethod
    def getByUsername(username):
        db = UsersDB.getInstance()
        expression = QueryExpression()
        expression.fromTable('users')
        expression.where('username', '=', username)
        result = db.query(expression.toSQL())

        if (len(result) == 0):
            return None

        if (len(result) > 1):
            raise ValueError('Invalid database state: Duplicate usernames')

        data = result[0]
        user = UserModel.fromDatabase(data)
        return user




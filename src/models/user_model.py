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
from datetime import datetime, timedelta
from functools import wraps

class UserModel(Model):

    @classmethod
    def model_props(cls):
        return [
            'username', 'email', 'password', 'project', 'requests_limit',
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

    def isAdmin(self):
        return self.role == 'admin'

    def block(self):
        self.status = 'blocked'

    def activate(self):
        self.status = 'active'

    def logRequest(self):
        if self.requests_made < self.requests_limit:
            self.requests_made += 1

        if self.last_request_datetime is None:
            self.last_request_datetime = datetime.now()
        else:
            this_month = datetime.now().month
            last_month = self.last_request_datetime.month

            this_year = datetime.now().year
            last_year = self.last_request_datetime.year

            if this_month > last_month or this_year > last_year:
                self.requests_made = 0
          
    @classmethod
    def getByUsername(cls, username):
        return super(UserModel, cls).getByAttributeSingle('username', username)


    @classmethod
    def fromDatabase(cls, row):
        model = super(UserModel, cls).fromDatabase(row)
        if model.last_request_datetime is not None:
            model.last_request_datetime = datetime.strptime(model.last_request_datetime, "%Y-%m-%d %H:%M:%S.%f")
        return model

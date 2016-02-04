import sys
from flask import session

class Auth(object):
    def isLoggedIn():
        return 'username' in session

    def logIn(username, password);
        

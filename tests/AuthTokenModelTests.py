import unittest
import os
import sys
import datetime
from datetime import timedelta

modelsPath = os.path.realpath('../src/models')
sys.path.append(modelsPath)

dbPath = os.path.realpath('../src/db')
sys.path.append(dbPath)

from users_db import UsersDB
from auth_token_model import AuthTokenModel

class AuthTokenModelTests(unittest.TestCase):

    # Runs once per class
    @classmethod
    def setUpClass(cls):
        UsersDB.getInstance().reset()  

    def test_create_token(self):
        tok = 'kksdfsdfsdjfjsdkfj9887'
        timestamp = datetime.datetime.now()
        token = AuthTokenModel()
        token.user_id = 33
        token.token = tok
        token.expiration_timestamp = timestamp
        token.is_long_lasting = '1'
        token.updated = timestamp
        token.created = timestamp
        token.save()
	
        dbTokenRow = AuthTokenModel.getByAttributeSingle('token',tok)
    
        self.assertEqual(dbTokenRow.user_id, 33)
        self.assertEqual(dbTokenRow.token, tok)
        self.assertEqual(dbTokenRow.expiration_timestamp, timestamp)	
        self.assertEqual(dbTokenRow.is_long_lasting, 1)
        #self.assertEqual(dbTokenRow.updated, timestamp)
        #self.assertEqual(dbTokenRow.created, timestamp)

    def test_is_valid_true(self):
        tok = 'klowekoriweruuiweryu6767'
        timestamp = datetime.datetime.now()
        token = AuthTokenModel()
        token.user_id = 36
        token.token = tok
        token.expiration_timestamp = timestamp + timedelta(days = 1) + timedelta(hours = 2)
        token.is_long_lasting = '1'
        token.save()
	
        dbTokenRow = AuthTokenModel.getByAttributeSingle('token',tok)    
        

        self.assertEqual(dbTokenRow.isValid(), True)
		
    def test_is_valid_false(self):
        tok = 'ksejfiwejir873487347567'
        timestamp = datetime.datetime.now()
        token = AuthTokenModel()
        token.user_id = 36
        token.token = tok
        token.expiration_timestamp = timestamp + timedelta(days = -1) + timedelta(hours = 2)
        token.is_long_lasting = '1'
        token.save()
	
        dbTokenRow = AuthTokenModel.getByAttributeSingle('token',tok)    
        

        self.assertEqual(dbTokenRow.isValid(), False)
	
    def test_is_valid_when_times_are_equal(self):
        tok = '8645u6hjrthgjhretjhgjh'
        timestamp = datetime.datetime.now()
        token = AuthTokenModel()
        token.user_id = 37
        token.token = tok
        token.expiration_timestamp = timestamp
        token.is_long_lasting = '1'
        token.save()
	
        dbTokenRow = AuthTokenModel.getByAttributeSingle('token',tok)    
        
		#koga expiration date e ednakvo momentalnoto vreme, dava deka tokenot ne e validen
        self.assertEqual(dbTokenRow.isValid(), False)
		
    def test_extend(self):
        tok = '9458893457874587huhghbdfhg'
        timestamp = datetime.datetime.now()
        token = AuthTokenModel()
        token.user_id = 38
        token.token = tok
        token.expiration_timestamp = timestamp + timedelta(hours = 1)
        token.is_long_lasting = '1'
        token.save()
	
        dbTokenRow = AuthTokenModel.getByAttributeSingle('token',tok)    
		#ovde javuva greska : TypeError: unsupported operand type(s) for +: 'datetime.datetime' and 'int'
        dbTokenRow.extend()
        print dbTokenRow
		

if __name__ == '__main__':
    unittest.main()

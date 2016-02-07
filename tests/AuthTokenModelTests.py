import unittest
import os
import sys

modelsPath = os.path.realpath('../src/models')
sys.path.append(modelsPath)

dbPath = os.path.realpath('../src/db')
sys.path.append(dbPath)

from users_db import UsersDB
from auth_token_model import AuthTokenModel

class AuthTokenModelTests(unittest.TestCase):

  def test_create_token(self):
    token = AuthTokenModel()
    token.user_id = 122
    token.token = 'askjask98243874njsdkf'
    token.expiration_timestamp = '2016-02-07 15:00:00'
    token.is_long_lasting = 1
    token.updated = '2016-02-07 14:44:23'
    token.created = '2016-02-07 14:44:23'
    token.save()
	
    dbToken = AuthTokenModel.getByAttributeSingle(token.token,'askjask98243874njsdkf')
 
    self.assertEqual(dbToken.user_id, 122)
    self.assertEqual(dbToken.token, 'askjask98243874njsdkf')
    self.assertEqual(dbToken.expiration_timestamp, '2016-02-07 15:00:00')
    self.assertEqual(dbToken.is_long_lasting, 1)
    self.assertEqual(dbToken.updated, '2016-02-07 14:44:23')
    self.assertEqual(dbToken.created, '2016-02-07 14:44:23') 
     

if __name__ == '__main__':
    unittest.main()

import unittest
import os
import sys

modelsPath = os.path.realpath('../src/models')
sys.path.append(modelsPath)

dbPath = os.path.realpath('../src/db')
sys.path.append(dbPath)

from users_db import UsersDB
from user_model import UserModel

class UserTokenModelTests(unittest.TestCase):

    # Runs once per class
    @classmethod
    def setUpClass(cls):
        UsersDB.getInstance().reset()

    def test_create_user(self):
        username = 'user1'

        # Read parameters
        user = UserModel()
        user.username = username
        user.setPassword('000000')
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.status = 'active'
        user.role = 'admin'
        user.save()

        dbUser = UserModel.getByUsername(user.username)

        self.assertEqual(dbUser.username, username)
        self.assertEqual(dbUser.project, 'ReLDI')
        self.assertEqual(dbUser.requests_limit, 1000)
        self.assertEqual(dbUser.requests_made, 0)
        self.assertEqual(dbUser.status, 'active')
        self.assertEqual(dbUser.role, 'admin')

    def test_delete_user(self):
        username = 'user2'
        # Read parameters
        user = UserModel()
        user.username = username
        user.setPassword('000000')
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.status = 'active'
        user.role = 'admin'
        user.save()

        dbUser = UserModel.getByUsername(user.username)
        self.assertIsNotNone(dbUser)

        dbUser.delete()
        dbUser = UserModel.getByUsername(user.username)
        self.assertIsNone(dbUser);        

    def test_login_user(self):

        username = 'user3'
        password = '000000'
        # Read parameters
        user = UserModel()
        user.username = username
        user.setPassword(password)
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.status = 'active'
        user.role = 'admin'
        user.save()

        dbUser = UserModel.getByUsername(user.username)
        token = dbUser.generateToken(password)
        self.assertIsNotNone(token)

    def test_login_user_invalid(self):

        username = 'user4'
        password = '000000'
        # Read parameters
        user = UserModel()
        user.username = username
        user.setPassword(password)
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.status = 'active'
        user.role = 'admin'
        user.save()

        dbUser = UserModel.getByUsername(user.username)
        with self.assertRaises(ValueError):
            token = dbUser.generateToken('not this password')

    def test_update_user(self):
        username = 'user78'
        password = '000000'
        # Read parameters
        user = UserModel()
        user.username = username
        user.setPassword(password)
        user.project = 'ReLDI'
        user.requests_limit = 1000
        user.requests_made = 0
        user.status = 'active'
        user.role = 'admin'
        user.save()
		
        dbUser = UserModel.getByUsername(user.username) 	
		
        new_username = 'user787'
        dbUser.username = new_username
        dbUser.project = 'RelDI2'
        dbUser.requests_limit = 2000
        dbUser.requests_made = 4
        dbUser.status = 'block'
        dbUser.role = 'employe'
        dbUser.save()
		
        self.assertEqual(dbUser.username, 'user66')
        self.assertEqual(dbUser.project, 'ReLDI2')
        self.assertEqual(dbUser.requests_limit, 2000)
        self.assertEqual(dbUser.requests_made, 4)
        self.assertEqual(dbUser.status, 'block')
        self.assertEqual(dbUser.role, 'employe')
		
if __name__ == '__main__':
    unittest.main()
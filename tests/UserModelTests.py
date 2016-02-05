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



if __name__ == '__main__':
    unittest.main()
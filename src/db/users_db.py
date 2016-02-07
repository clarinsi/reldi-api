
# -*- coding: utf-8 -*-
import os
import sqlite3
import re
import sys

srcPath = os.path.realpath('../')
sys.path.append(srcPath)
from reldi_db import DB
from query_expression import QueryExpression

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class UsersDB(DB):
    '''Override database'''
    # Stores the connection
    _instance = None

    @staticmethod
    def getInstance():
        assetsPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../../assets/')
    
        databaseName = assetsPath + '/users';
        if (UsersDB._instance is None):
            UsersDB._instance = UsersDB(DB._THE_MAGIC_WORD)
            if (UsersDB._instance._connection is None):
                # Initialize connection
                UsersDB._instance._connection = sqlite3.connect(databaseName,isolation_level=None)
                UsersDB._instance._connection.text_factory = str
                UsersDB._instance._connection.row_factory = dict_factory
                UsersDB._instance._client = UsersDB._instance._connection.cursor()
            
            UsersDB._instance.__createTables()

        return UsersDB._instance

    def getInsertId(self):
        return self._client.lastrowid

    def reset(self):
        self.command("DROP TABLE IF EXISTS users")
        self.command("DROP TABLE IF EXISTS auth_tokens")
        self.__createTables()

    def __createTables(self):
        db = self.getInstance()
        # Create users table
        statement = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                project TEXT,
                requests_limit INTEGER NOT NULL,
                requests_made INTEGER NOT NULL DEFAULT 0,
                last_request_datetime TEXT,
                role TEXT NOT NULL,
                status TEXT NOT NULL,
                updated TEXT NOT NULL,
                created TEXT NOT NULL
                CHECK (role IN ("admin", "user"))
                CHECK (status IN ("pending", "blocked", "active"))
                
            );
        """
        db.command(statement)

        # Create tokens table
        statement = """
            CREATE TABLE IF NOT EXISTS auth_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT,
                expiration_timestamp TEXT,
                updated TEXT NOT NULL,
                created TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
                UNIQUE(user_id, token)
            );
        """
        db.command(statement)




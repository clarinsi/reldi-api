# -*- coding: utf-8 -*-

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Main database class
class DB(object):
    # Must be passed into the constructor. Ensures the constructor is private
    _THE_MAGIC_WORD = object()

    # Private object constructor
    def __init__(self, token):
        self._connection = None
        self._client = None
        if token is not self._THE_MAGIC_WORD:
            raise ValueError('This is a private constructor. Plase use ::getInstance()')

    @staticmethod
    def set_row_factory(connection):
        connection.row_factory = dict_factory

    # Method to execute sql query
    def query(self, sql):
        '''Execute an SQL query'''
        if not self._client:
            raise ValueError("Client not initialized") 

        self._client.execute(sql)
        self._connection.commit()
        return self._client.fetchall()

    # Method to execute sql command
    def command(self, sql, params = ()):
        '''Execute an SQL query'''
        if not self._client:
            raise ValueError("Client not initialized")

        self._client.execute(sql, params)
        self._connection.commit()

    # Method to execute sql command
    def script(self, sql):
        '''Execute an SQL query'''
        if not self._client:
            raise ValueError("Client not initialized")

        self._client.executescript(sql)
        self._connection.commit()

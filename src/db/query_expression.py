# -*- coding: utf-8 -*-

# Main lexicon class
class QueryExpression(object):
    '''A class for building an abstract query expression'''

    def __init__(self):
        self.__select = []
        self.__from = None
        self.__where = []

    def select(self, fields):
        self.__select = fields
        return self

    def fromTable(self, table):
        self.__from = table
        return self;

    def where(self, field, operator, value):
        expression = "{0} {1} '{2}'".format(field, operator, value)
        self.__where.append(expression)
        return self

    def toSQL(self):

        # Ensure table is set
        if self.__from is None:
            raise ValueError('No table selected')

        # Build select part
        sql = '';
        if len(self.__select) == 0:
            sql = 'SELECT *'
        else:
            sql = 'SELECT ' + ", ".join(self.__select)

        # Build from part
        sql += ' FROM ' + self.__from

        # Build where part
        if len(self.__where) > 0:
            sql += ' WHERE ' + " AND ".join(self.__where)

        return sql

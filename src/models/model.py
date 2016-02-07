import sys, os

dbpath = os.path.realpath('../db')
sys.path.append(dbpath)
import json
from datetime import datetime
from users_db import UsersDB
from query_expression import QueryExpression


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class Model(object):

    def __init__(self):

        self.all_props = self.__class__.model_props() + ['created', 'updated']
        self.pk = self.__class__.primary_key()
        self.tn = self.__class__.table_name()

        for prop in self.all_props + [self.pk]:
            setattr(self, prop, None)

    def save(self):
        if getattr(self, self.pk) is None:
            self.insert()
        else:
            self.update()

    def delete(self):
        sql = "DELETE FROM {0} WHERE {1} = ?".format(self.tn, self.pk)
        db = UsersDB.getInstance()
        pk = getattr(self, self.pk)
        db.command(sql, (pk,))
        setattr(self, self.pk, None)

    def insert(self):
        self.created = datetime.now()
        self.updated = datetime.now()
        # Dict
        dbModel = self.toDbModel()

        dbModelTuple = [(key, value) for key, value in dbModel.iteritems()]
        dbModelKeys = [key for key, value in dbModelTuple]
        dbModelValues = [value for key, value in dbModelTuple]
        placeholders = ["?" for k in dbModelKeys]
        
        sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(self.tn, ", ".join(dbModelKeys), ", ".join(placeholders))
        db = UsersDB.getInstance()
        db.command(sql, dbModelValues)
        self.id = db.getInsertId()

    def update(self):
        if not hasattr(self, self.pk) or getattr(self, self.pk) is None:
            raise ValueError('Invalid operation, primary key is not.')

        self.updated = datetime.now()
        
        dbModel = self.toDbModel()
        dbModelTuple = [(key, value) for key, value in dbModel.iteritems()]
        dbModelKeys = [key for key, value in dbModelTuple]
        dbModelValues = [value for key, value in dbModelTuple]
        
        sql = "UPDATE {0} SET ".format(self.tn)
        sql += ", ".join(map(lambda x: "{0}=?".format(x), dbModelKeys))
        db = UsersDB.getInstance()
        db.command(sql, dbModelValues);

    def toDbModel(self):
        result = {}
        for prop in self.all_props:
            result[prop] = getattr(self, prop)

        return result

    def __str__(self):
        d = {
            self.primary_key(): getattr(self, self.pk)
        }
        for prop in self.all_props:
            d[prop] = getattr(self, prop)

        return json.dumps(d, ensure_ascii = False, indent = 4, default = date_handler)

    @classmethod
    def getByAttributeSingle(cls, key, value):
        db = UsersDB.getInstance()
        expression = QueryExpression()
        expression.fromTable(cls.table_name())
        expression.where(key, '=', value)
        result = db.query(expression.toSQL())

        if (len(result) == 0):
            return None

        if (len(result) > 1):
            raise ValueError('Query returned multiple rows')

        data = result[0]
        o = cls.fromDatabase(data)
        return o

    @classmethod
    def getByAttribute(cls, key, value):
        db = UsersDB.getInstance()
        expression = QueryExpression()
        expression.fromTable(cls.table_name())
        expression.where(key, '=', value)
        result = db.query(expression.toSQL())

        if (len(result) == 0):
            return []

        data = result
        return map(lambda x: cls.fromDatabase(x), result)

    @classmethod
    def getByAttributesSingle(cls, keys, values):
        db = UsersDB.getInstance()
        expression = QueryExpression()
        expression.fromTable(cls.table_name())
        for idx, key in enumerate(keys):
            expression.where(key, '=', values[idx])

        result = db.query(expression.toSQL())

        if (len(result) == 0):
            return None

        if (len(result) > 1):
            raise ValueError('Query returned multiple rows')

        data = result[0]
        o = cls.fromDatabase(data)
        return o


    @classmethod
    def fromDatabase(cls, row):
        all_props = cls.model_props() + ['created', 'updated']

        o = cls()
        setattr(o, cls.primary_key(), row[cls.primary_key()])
        for prop in all_props:
            setattr(o, prop, row[prop])
        return o

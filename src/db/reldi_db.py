# -*- coding: utf-8 -*-
import os
import sqlite3
import re

def regexp(expr, item):
	reg = re.compile(expr)
	return reg.search(item) is not None

# Main database class
class DB(object):
	'''Reldi database class'''

	# Object constructor
	def __init__(self, database, row_factory=None):
		'''Create connection and cursor'''
		# Connect to file database
		#fileConnection = sqlite3.connect(database)
		#fileConnection.text_factory = str
		# Create an in-memory database
		#self.connection = sqlite3.connect(':memory:')

		# Copy file database to memory
		#query = "".join(line for line in fileConnection.iterdump())
		#self.connection.executescript(query)

		self.connection = sqlite3.connect(database)
		if (row_factory is not None):
			self.connection.row_factory = row_factory

		self.connection.create_function("REGEXP", 2, regexp)
		self.connection.text_factory = str
		self.client = self.connection.cursor()

	# Object destructor
	def __del__(self):
		'''Close the database connection'''
		self.connection.close()

	# Method to execute sql query
	def query(self, sql):
		'''Execute an SQL query'''
		if not self.client:
			return False

		self.client.execute(sql)
		self.connection.commit()
		return self.client.fetchall()

	# Method to execute sql command
	def command(self, sql, params = ()):
		'''Execute an SQL query'''
		if not self.client:
			raise ValueError("Client not initialized") 
			return False

		self.client.execute(sql, params)
		self.connection.commit()

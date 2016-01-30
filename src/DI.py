# -*- coding: utf-8 -*-
import os
import sys

class DependencyContainer(object):
	'''Class segmenter'''

	def __init__(self, lazy = False):
		self.lazy = lazy
		self.initializers = {}
		self.instances = {}
		
	def registerInstance(self, key, function):
		if key in self.initializers:
			raise ValueError('Instance already defined')

		self.initializers[key] = function
		if not self.lazy:
			self.instances[key] = function()

	def getInstance(self, key):
		if (key not in self.instances):
			function = self.initializers[key]
			self.instances[key] = function()

		return self.instances[key]
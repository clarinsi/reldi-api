# -*- coding: utf-8 -*-


class DependencyContainer(object):
    """
    A dependency injection container
    """
    def __init__(self, lazy=False):
        """
        :param lazy: determines whether instances will be created lazyly on demand
        """
        self.lazy = lazy
        self.initializers = {}
        self.instances = {}

    def __setitem__(self, key, function):
        """
        Registers an instance in the container

        :param key: instance key
        :param function: a function which constructs an object attached to the key
        :raises keyError: raises an exception
        """
        if key in self.initializers:
            raise ValueError('Instance already defined')

        self.initializers[key] = function
        if not self.lazy:
            self.instances[key] = function()

    def __getitem__(self, key):
        """
        Get an instance from the container

        :param key: determines whether instances will be created lazyli on demand
        :raises keyError: raises an exception
        """
        if key not in self.initializers:
            raise ValueError('Instance does not exist')

        if key not in self.instances:
            function = self.initializers[key]
            self.instances[key] = function()

        return self.instances[key]

#!/usr/bin/env python3
"""
This module implements a FIFO cache.
"""
from typing import Any
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ A class that is a caching system using FIFO
    """

    def __init__(self):
        super().__init__()

        self.__qeue = []

    def put(self, key, item: Any) -> None:
        """A method that adds an item to the cache
        """

        if None in (key, item):
            return

        if key in self.__qeue:
            self.__qeue.pop(self.__qeue.index(key))
        self.__qeue.append(key)

        if (len(self.cache_data.keys()) >= self.MAX_ITEMS and
                key not in self.cache_data):

            discarded_key = self.__qeue[0]
            del self.cache_data[discarded_key]
            self.__qeue.pop(0)

            print(f"DISCARD: {discarded_key}")

        self.cache_data.update({key: item})

    def get(self, key):
        """ A method that gets an item from the cache
        """

        return self.cache_data.get(key)

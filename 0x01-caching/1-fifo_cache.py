#!/usr/bin/env python3
"""
This module implements a FIFO cache.
"""
from base_caching import BaseCaching
from typing import Any


class FIFOCache(BaseCaching):
    """ A class that is a caching system using FIFO
    """

    def __init__(self):
        super().__init__()

        self.__qeue = []

    def put(self, key: Any, item: Any) -> None:
        """A method that adds an item to the cache
        """

        if None in (key, item):
            return

        if key not in self.__qeue:
            self.__qeue.append(key)
        # print(self.__qeue)

        if (len(self.cache_data.keys()) >= self.MAX_ITEMS and
                key not in self.cache_data):

            discarded_key = self.__qeue[0]
            del self.cache_data[discarded_key]
            self.__qeue.pop(0)

            print(f"DISCARD {discarded_key}")

        self.cache_data.update({key: item})

    def get(self, key: Any) -> Any:
        """ A method that gets an item from the cache
        """

        return self.cache_data.get(key)
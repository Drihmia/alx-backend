#!/usr/bin/python3
""" BaseCaching module
"""
from typing import Any
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ A class that is a caching system
    """
    def put(self, key: Any, item: Any) -> None:
        """ A method that adds an item to the cache
        """
        if None in (key, item):
            return
        self.cache_data.update({key: item})

    def get(self, key: Any) -> Any:
        """ A method that gets an item from the cache
        """

        return self.cache_data.get(key)

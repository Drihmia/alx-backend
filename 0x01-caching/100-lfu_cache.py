#!/usr/bin/env python3
"""
This module implements a LFU cache.
"""
from typing import Any
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ A class that is a caching system using LFU
    """

    def __init__(self):
        super().__init__()

        self.__qeue = [[]]

    def put(self, key, item: Any) -> None:
        """A method that adds an item to the cache
        """

        if None in (key, item):
            return

        self.__qeue = self.clean(self.__qeue)

        i = 0
        found = False
        for i in range(len(self.__qeue)):
            if key in self.__qeue[i]:
                found = True
                break

        if found:
            self.__qeue[i].pop(self.__qeue[i].index(key))
            self.__qeue[i + 1].append(key)
            self.__qeue = self.clean(self.__qeue)

        if (len(self.cache_data.keys()) >= self.MAX_ITEMS and
                key not in self.cache_data):

            i = 0
            while len(self.__qeue[i]) == 0:
                i += 1

            discarded_key = self.__qeue[i][0]
            del self.cache_data[discarded_key]
            self.__qeue[i].pop(0)

            print(f"DISCARD: {discarded_key}")
        if not found:
            self.__qeue[0].append(key)

        self.__qeue = self.clean(self.__qeue)
        self.cache_data.update({key: item})
        # print(self.__qeue)
        # print(self.cache_data)

    def get(self, key):
        """ A method that gets an item from the cache
        """

        length = len(self.__qeue)
        if not length:
            return None

        # if len(self.__qeue[0]) == 0 and len(self.__qeue) > 1:
            # self.__qeue.pop(0)
        self.__qeue = self.clean(self.__qeue)

        length = len(self.__qeue)
        if not length:
            return None  # "----------"

        # print(self.__qeue)
        i = 0
        found = False
        for i in range(length):
            if key in self.__qeue[i]:
                found = True
                break

        # print(f"i = {i}")
        if not found:
            return None  # f"{key} Not found"

        self.__qeue[i].pop(self.__qeue[i].index(key))

        if (i + 1) == length:
            self.__qeue.append([])
        self.__qeue[i + 1].append(key)
        self.__qeue = self.clean(self.__qeue)
        return self.cache_data.get(key)

    def clean(self, lst_list):
        """ Return list of indexes of empty rows in descending order """
        idx_to_clean = [
            i for i in range(1, len(lst_list)) if len(lst_list[i]) == 0][::1]

        for idx in idx_to_clean:
            lst_list.pop(idx)

        if not len(lst_list):
            return [[]]

        return lst_list

#!/usr/bin/env python3
"""
This module contains the following:
 + index_range : A function.
 + Server : A class.
"""
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    A function that return a tuple containing start index and an end
    index corresponding  to the range of indexes

    Notes: page numbers are 1-indexed
    """

    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.dataset()

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        A method that returns a slice of file based on the inputs given.
        """
        if not all([isinstance(page, int), isinstance(page_size, int)]):
            raise AssertionError(f"{page} or {page_size} is not a integer")

        if not all([page > 0, page_size > 0]):
            raise AssertionError(
                f"{page} or {page_size} is not greater than 0")

        start_index, end_index = index_range(page, page_size)

        if self.__dataset is None:
            return [[]]
        return self.__dataset[start_index: end_index]

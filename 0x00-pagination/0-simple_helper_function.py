#!/usr/bin/env python3
"""
This module contains a function called : index_range
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    A function that return a tuple containing start index and an end
    index corresponding  to the range of indexes

    Notes: page numbers are 1-indexed
    """

    # if not page:
    # return (0, page_size)

    return (((page - 1) * page_size), (page * page_size))

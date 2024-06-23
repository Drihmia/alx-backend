#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:

        if not all([isinstance(index, int), isinstance(page_size, int)]):
            raise AssertionError(f"{index} or {page_size} is not a integer")

        if not all([index >= 0, page_size > 0]):
            raise AssertionError(
                f"{index} or {page_size} is not greater than 0")

        indexed_dataset = self.indexed_dataset()

        if indexed_dataset is None or not len(indexed_dataset):
            return {
                "index": index,
                "page_size": page_size,
                "next_index": None,
                "data": []
            }

        largest_index = sorted(indexed_dataset.keys())[-1]
        if index >= largest_index:
            raise AssertionError(f"{index} not a valid index")

        next_index = None
        data = []
        offset = 0
        for pos in range(index, index + page_size):
            idx = offset + pos
            if idx not in indexed_dataset:

                # moving the offset until we find next idx.
                while True:
                    idx = offset + pos

                    if idx in indexed_dataset:
                        break

                    if idx >= largest_index:
                        break
                    offset += 1

            data.append(indexed_dataset[idx])
            next_index = idx + 1

        # print(f"largest_index: {largest_index}")
        # print(f"length: {len(indexed_dataset)}")
        return {
            "index": index,
            "page_size": page_size,
            "next_index": next_index,
            "data": data
        }

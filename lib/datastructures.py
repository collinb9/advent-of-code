""" Some convenience classes for working with different datastructures """
from typing import List
import dataclasses
import itertools


@dataclasses.dataclass
class Array:
    """A 2-d array"""

    data: List

    def __post_init__(self):
        self.x = len(self.data[0])
        self.y = len(self.data)
        self.grid = itertools.product(range(self.y), range(self.x))

    def loc(self, i, j):
        return self.data[j][i]

    def find_value(self, coord: List[int]):
        return self.loc(coord[0], coord[1])

    def find_adjacent(self, i, j):
        loc = [
            (i, min(j + 1, self.y - 1)),
            (i, max(0, j - 1)),
            (max(0, i - 1), j),
            (min(i + 1, self.x - 1), j),
        ]
        return [ll for ll in loc if ll != (i, j)]

    def neighbourhood(self, i, j):
        loc = {
            (i, min(j + 1, self.y - 1)),
            (i, max(0, j - 1)),
            (max(0, i - 1), max(0, j - 1)),
            (max(0, i - 1), j),
            (max(0, i - 1), min(j + 1, self.y - 1)),
            (min(i + 1, self.x - 1), max(0, j - 1)),
            (min(i + 1, self.x - 1), j),
            (min(i + 1, self.x - 1), min(j + 1, self.y - 1)),
        }
        return [ll for ll in loc if ll != (i, j)]

    def find_row(self, i, j):
        return [(k, j) for k in range(data.x)]

    def find_column(self, i, j):
        return [(i, k) for k in range(data.y)]

    def find_all_left(self, i, j):
        return [(i - k, j) for k in range(1, i + 1)][::-1]

    def find_all_right(self, i, j):
        return [(i + k, j) for k in range(1, self.x - i)]

    def find_all_down(self, i, j):
        return [(i, j + k) for k in range(1, self.y - j)]

    def find_all_up(self, i, j):
        return [(i, j - k) for k in range(1, j + 1)][::-1]

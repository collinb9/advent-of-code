""" Some convenience classes for working with different datastructures """
from typing import List
import dataclasses
import itertools


@dataclasses.dataclass
class Array:
    """A 2-d array"""

    data: List

    up, down, left, right = (0, -1), (0, 1), (-1, 0), (1, 0)

    @property
    def grid(self):
        return itertools.product(range(self.x), range(self.y))

    @property
    def x(self):
        return len(self.data[0])

    @property
    def y(self):
        return len(self.data)

    def __contains__(self, point):
        i, j = point
        return (0 <= i < self.x) and (0 <= j < self.y)

    def loc(self, i, j):
        return self.data[j][i]

    def find_value(self, coord: List[int]):
        return self.loc(coord[0], coord[1])

    @classmethod
    def shift(cls, coord, shift):
        return (coord[0] + shift[0], coord[1] + shift[1])

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

    @classmethod
    def line(cls, start, end):
        minx = min(start[0], end[0])
        maxx = max(start[0], end[0])
        miny = min(start[1], end[1])
        maxy = max(start[1], end[1])
        if start[0] == end[0]:
            return [(start[0], j) for j in range(miny, maxy + 1)]
        else:
            return [(i, start[1]) for i in range(minx, maxx + 1)]

    @property
    def columns(self):
        return [self.find_column(i) for i in range(self.x)]

    def find_row(self, j):
        return [(k, j) for k in range(self.x)]

    def find_column(self, i):
        return [(i, k) for k in range(self.y)]

    def find_all_left(self, i, j):
        return [(i - k, j) for k in range(1, i + 1)][::-1]

    def find_all_right(self, i, j):
        return [(i + k, j) for k in range(1, self.x - i)]

    def find_all_down(self, i, j):
        return [(i, j + k) for k in range(1, self.y - j)]

    def find_all_up(self, i, j):
        return [(i, j - k) for k in range(1, j + 1)][::-1]

    def pprint(self):
        for row in self.data:
            print("".join(row))

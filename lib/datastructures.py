""" Some convenience classes for working with different datastructures """
from typing import List, Any, Tuple
import dataclasses
import itertools


@dataclasses.dataclass(order=True)
class PrioritizedItem:
    priority: Tuple[int]
    item: Any = dataclasses.field(compare=False)


@dataclasses.dataclass
class BaseArray:
    """A 2-d array"""

    xx: int = 0
    yy: int = 0

    sentinel = "~"

    up, down, left, right, up_right, down_right, down_left, up_left = (
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
        (1, -1),
        (1, 1),
        (-1, 1),
        (-1, -1),
    )

    @classmethod
    def shift(cls, coord, shift):
        return (coord[0] + shift[0], coord[1] + shift[1])

    @property
    def x(self):
        return self.xx

    @property
    def y(self):
        return self.yy

    def __contains__(self, point):
        i, j = point
        return (0 <= i < self.x) and (0 <= j < self.y)

    @property
    def grid(self):
        return itertools.product(range(self.x), range(self.y))

    def find_adjacent(self, i, j):
        loc = [
            (i, min(j + 1, self.y - 1)),
            (i, max(0, j - 1)),
            (max(0, i - 1), j),
            (min(i + 1, self.x - 1), j),
        ]
        return [ll for ll in loc if ll != (i, j)]

    def find_adjacent_with_boundary(self, i, j):
        loc = [
            (i, j + 1),
            (i - 1, j),
            (i, j - 1),
            (i + 1, j),
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

    def neighbourhood_with_boundary(self, i, j):
        loc = {
            (i, j + 1),
            (i - 1, j + 1),
            (i - 1, j),
            (i - 1, j - 1),
            (i, j - 1),
            (i + 1, j - 1),
            (i + 1, j),
            (i + 1, j + 1),
        }
        return [ll for ll in loc if ll != (i, j)]


@dataclasses.dataclass
class AbstractArray(BaseArray):
    """A 2-d array, only storing some metadata"""

    data: dict = dataclasses.field(default_factory=dict)

    def loc(self, i, j, empty="."):
        if j < 0 or j > self.y or i < 0 or i > self.x:
            return self.sentinel
        return self.data.get((i, j), empty)


@dataclasses.dataclass
class Array(BaseArray):
    """A 2-d array stored as a list of lists"""

    data: List = dataclasses.field(default_factory=list)

    @property
    def x(self):
        return len(self.data[0])

    @property
    def y(self):
        return len(self.data)

    def loc(self, i, j):
        if j < 0 or j >= self.y or i < 0 or i >= self.x:
            return self.sentinel
        return self.data[j][i]

    def find_value(self, coord: List[int]):
        return self.loc(coord[0], coord[1])

    @classmethod
    def from_dict(cls, data):
        max_x = max(data)[0]
        max_y = max(data, key=lambda x: x[1])[1]
        _array = [["."] * (max_x + 1) for _ in range(max_y + 1)]
        for key, value in data.items():
            _array[key[1]][key[0]] = str(value)
        return cls(data=_array)

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
            print("".join(map(str, row)))

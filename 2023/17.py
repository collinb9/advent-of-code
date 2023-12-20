import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array
import itertools
import queue
import collections

from dataclasses import dataclass, field
from typing import Any, Tuple


@dataclass(order=True)
class PrioritizedItem:
    priority: Tuple[int]
    item: Any = field(compare=False)


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, line.replace("\n", ""))) for line in fp.readlines()]

    return data


def clockwise(direction):
    direction = complex(direction[0], -1 * direction[1])
    rotation = complex(0, -1)
    res = direction * rotation
    return (int(res.real), int(res.imag))


def anticlockwise(direction):
    direction = complex(direction[0], -1 * direction[1])
    rotation = complex(0, 1)
    res = direction * rotation
    return (int(res.real), int(res.imag))


def adjacent(direction):
    if direction is None:
        return [Array.right, Array.down]
    _clockwise = clockwise(direction)
    _anticlockwise = anticlockwise(direction)
    return [_clockwise, direction, _anticlockwise]


def search(data, start_point, _max=3, _min=0):
    """
    Dijkstra

    Perform the standard dijktra on a grid where each node encodes the
    xy-coordinates as well as the current direction and the count of number of
    moves since the direction was last changed
    """
    sentinel = sum(itertools.chain.from_iterable(data.data))

    distances = collections.defaultdict(lambda: sentinel)
    distances[(start_point, 0, None)] = 0
    priority_queue = queue.PriorityQueue()
    priority_queue.put(PrioritizedItem(priority=0, item=(0, start_point, None)))
    seen = set()
    while not priority_queue.empty():
        priority_item = priority_queue.get()
        _distance = priority_item.priority
        _count, _point, _direction = priority_item.item
        if _point == (data.x - 1, data.y - 1):
            if _count < _min - 1:
                continue
            break
        if _count < _min - 1 and _direction is not None:
            next_directions = [_direction]
        else:
            next_directions = adjacent(_direction)
        for next_direction in next_directions:
            next_point = (_point[0] + next_direction[0], _point[1] + next_direction[1])
            if next_direction == _direction:
                count = _count + 1
            else:
                count = 0
            if count >= _max:
                continue
            if next_point in data and (_point, _count, _direction) not in seen:
                d = _distance + data.loc(*next_point)
                if d <= distances[(next_point, count, next_direction)]:
                    distances[(next_point, count, next_direction)] = d

                    priority_queue.put(
                        PrioritizedItem(
                            priority=d,
                            item=(
                                count,
                                next_point,
                                next_direction,
                            ),
                        )
                    )
        seen.add((_point, _count, _direction))
    return _distance


def main(fpath):
    data = Array(read_data(fpath))
    ans1 = search(data, (0, 0))
    ans2 = search(data, (0, 0), _max=10, _min=4)
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

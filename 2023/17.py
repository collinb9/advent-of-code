import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array
import itertools
import queue


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, line.replace("\n", ""))) for line in fp.readlines()]

    return data


def clockwise(direction):
    return direction


def anticlockwise(direction):
    return direction


def adjacent(data, current, direction):
    _clockwise = anticlockwise(direction)
    _anticlockwise = anticlockwise(direction)
    return set(
        [
            (current[0] + _clockwise[0], current[1] + _clockwise[1]),
            (current[0] + direction[0], current[1] + direction[1]),
            (current[0] + _anticlockwise[0], current[1] + _anticlockwise[1]),
        ]
    )


def search(data, point, direction):
    """
    Dijkstra
    """
    sentinel = sum(itertools.chain.from_iterable(data.data))
    distances = [[sentinel for _ in range(data.x)] for _ in range(data.y)]
    distances[0][0] = 0
    priority_queue = queue.PriorityQueue()
    priority_queue.put((point, direction))
    seen = set()
    while not priority_queue.empty():
        _point, _direction = priority_queue.get()
        for next_point in adjacent(data, _point, _direction):
            if next_point not in seen:
            #     d = current_distance + data[jj][ii]
            #     if d < distances[jj][ii]:
            #         distances[jj][ii] = d
            #         priority_queue.put((distances[jj][ii], (ii, jj)))
        seen.add(_point)
    return distances[yy - 1][xx - 1]


def main(fpath):
    data = Array(read_data(fpath))
    # data.pprint()
    ans1 = search(data, (0, 0), Array.right)
    return ans1, 0


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

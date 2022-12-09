import sys
import os
import copy
import itertools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split(" ") for line in fp.readlines()]
    directions = itertools.chain.from_iterable(
        [[direction] * int(size) for direction, size in data]
    )

    return directions


def main(fpath):
    DIRS = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    directions = read_data(fpath)
    rope = [(0, 0) for _ in range(10)]
    visited = set()
    tail_visited = set()
    for direction in directions:
        _direction = DIRS[direction]
        for i in range(len(rope) - 1):
            if i == 0:
                rope[i] = Array.shift(rope[i], _direction)
            _direction = (
                rope[i][0] - rope[i + 1][0],
                rope[i][1] - rope[i + 1][1],
            )
            if abs(_direction[0]) > 1 or abs(_direction[1]) > 1:
                _direction = (
                    int(_direction[0] / max(1, abs(_direction[0]))),
                    int(_direction[1] / max(1, abs(_direction[1]))),
                )
                rope[i + 1] = Array.shift(rope[i + 1], _direction)
        # Part 1
        visited.add(str(rope[1]))
        # Part 2
        tail_visited.add(str(rope[-1]))

    return len(visited), len(tail_visited)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

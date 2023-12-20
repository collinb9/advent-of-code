import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array
import re

DIRECTIONS = {"R": Array.right, "U": Array.up, "D": Array.down, "L": Array.left}
DIRECTION_CODES = ["R", "D", "L", "U"]


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split() for line in fp.readlines()]

    return data


def calculate_area(path):
    """Use a formula derived using Green's theorem to calculate the area"""
    res = 0
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        res += (x1 + x2) * (y2 - y1) / 2
    return abs(res)


def walk_path(data):
    path = []
    start = (0, 0)
    current = start
    path.append(current)
    circumference = 0
    for direction, count in data:
        count = int(count)
        circumference += count
        _direction = DIRECTIONS[direction]
        current = (
            current[0] + count * _direction[0],
            current[1] + count * _direction[1],
        )
        path.append(current)
    return path, circumference


def main(fpath):
    data = read_data(fpath)
    # Part 1
    data1 = [[direction, count] for direction, count, _ in data]
    path, circumference = walk_path(data1)
    area = calculate_area(path)
    ans1 = area + circumference / 2 + 1

    # Part 2
    pattern = r"\(#(.*)\)"
    hex_data = [re.search(pattern, _hex).group(1) for *_, _hex in data]
    data2 = []
    for item in hex_data:
        number, code = int(item[:-1], 16), int(item[-1])
        data2.append([DIRECTION_CODES[code], number])
    path, circumference = walk_path(data2)
    area = calculate_area(path)
    ans2 = area + circumference / 2 + 1
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

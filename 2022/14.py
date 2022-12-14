import sys
import os
import copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [
            list(
                map(
                    lambda x: tuple(map(int, x.split(","))), item.split(" -> ")
                )
            )
            for item in fp.read().split("\n")
            if item
        ]

    return data


def simulate(rocks: set, floor: int):
    sand = (500, 0)
    sands = 0
    void = True
    while True:
        if sand[1] >= floor:
            if void:
                yield sands
                void = False
            rocks.add((sand[0], floor + 2))
            rocks.add((sand[0] + 1, floor + 2))
            rocks.add((sand[0] - 1, floor + 2))
        if (sand[0], sand[1] + 1) in rocks:
            if (sand[0] - 1, sand[1] + 1) in rocks:
                if (sand[0] + 1, sand[1] + 1) in rocks:
                    sands += 1
                    rocks.add(sand)
                    if sand[1] == 0:
                        break
                    sand = (500, 0)
                else:
                    sand = (sand[0] + 1, sand[1] + 1)
            else:
                sand = (sand[0] - 1, sand[1] + 1)
        else:
            sand = (sand[0], sand[1] + 1)
    yield sands


def main(fpath):
    data = read_data(fpath)

    rocks = set()
    for path in data:
        for i in range(len(path) - 1):
            full_line = set(Array.line(path[i], path[i + 1]))
            rocks = rocks.union(full_line)

    floor = max(rocks, key=lambda x: x[1])[1]
    gen = simulate(rocks, floor)
    return next(gen), next(gen)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

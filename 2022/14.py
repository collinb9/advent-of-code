import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    data = [list(map(lambda x: tuple(map(int, x.split(","))), item.split(" -> "))) for item in data]

    return data


def main(fpath):
    data = read_data(fpath)

    rocks = set()
    for path in data:
        for i in range(len(path) - 1):
            full_line = set(Array.line(path[i], path[i+1]))
            rocks = rocks.union(full_line)

    sentinel = max(rocks, key =  lambda x: x[1])[1]
    sand = (500, 0)
    sands = 0
    while True:
        if sand[1] >= sentinel:
            # break
            rocks.add((sand[0], sentinel + 2))
            rocks.add((sand[0] + 1, sentinel + 2))
            rocks.add((sand[0] - 1, sentinel + 2))
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
    return sands, 0


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

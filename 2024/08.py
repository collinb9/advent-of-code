import sys
import re
from lib.datastructures import Array
from collections import defaultdict
import itertools

EMPTY = "."


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line) for line in fp.read().splitlines()]

    return data


def find_antipoles(array, antenna1, antenna2, part=1):
    xdiff = antenna2[0] - antenna1[0]
    ydiff = antenna1[1] - antenna2[1]
    res = set()
    if part == 1:
        antipole1 = (
            antenna1[0] - xdiff,
            antenna1[1] + ydiff,
        )
        antipole2 = (
            antenna2[0] + xdiff,
            antenna2[1] - ydiff,
        )
        if antipole1 in array:
            res.add(antipole1)
        if antipole2 in array:
            res.add(antipole2)
    elif part == 2:
        res.add(antenna1)
        res.add(antenna2)
        inc = 1
        while True:
            antipole = (
                antenna1[0] + inc * xdiff,
                antenna1[1] - inc * ydiff,
            )
            if antipole in array:
                res.add(antipole)
            else:
                break
            inc += 1
        inc = 1
        while True:
            antipole = (
                antenna1[0] - inc * xdiff,
                antenna1[1] + inc * ydiff,
            )
            if antipole in array:
                res.add(antipole)
            else:
                break
            inc += 1

    return res


def main(fpath):
    data = read_data(fpath)
    array = Array(data)
    array.sentinel = "~"

    ans1 = 0
    ans2 = 0

    # Find all antennas
    antennas = defaultdict(set)
    for xx, yy in array.grid:
        value = array.loc(xx, yy)
        if value != EMPTY:
            antennas[value].add((xx, yy))

    antipoles1 = set()
    antipoles2 = set()
    for _, antennas in antennas.items():
        for perm in itertools.combinations(antennas, 2):
            _antipoles1 = find_antipoles(array, *perm, part=1)
            antipoles1.update(_antipoles1)
            _antipoles2 = find_antipoles(array, *perm, part=2)
            antipoles2.update(_antipoles2)
    ans1 = len(antipoles1)
    ans2 = len(antipoles2)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

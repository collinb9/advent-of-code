import sys
from lib.utils import ints
from lib.datastructures import Array
import operator
import functools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [ints(line) for line in fp.read().splitlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    # print(data)

    ans1 = 0
    ans2 = 0

    quadrants = [0, 0, 0, 0]

    xx = 101
    yy = 103
    steps = 100

    directions = dict()
    for line in data:
        ii, jj, vi, vj = line
        directions[(ii, jj)] = (vi, vj)
        ii = (ii + steps * vi) % xx
        jj = (jj + steps * vj) % yy
        if ii < xx // 2:
            if jj < yy // 2:
                quadrants[0] += 1
            elif jj > yy // 2:
                quadrants[1] += 1
        elif ii > xx // 2:
            if jj < yy // 2:
                quadrants[2] += 1
            elif jj > yy // 2:
                quadrants[3] += 1

    ans1 = functools.reduce(operator.mul, quadrants, 1)

    ### Part 2 - Manually inspect output

    # seconds = 10000
    # for inc in range(1, seconds):
    #     positions = dict()
    #     print("Second:", inc)
    #     for (ii, jj), (vi, vj) in directions.items():
    #         positions[((ii + inc * vi) % xx, (jj + inc * vj) % yy)] = "#"
    #     array = Array.from_dict(positions)
    #     array.pprint()

    ans2 = 7603

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

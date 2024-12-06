import sys
import re
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    array = Array(data)

    ans1 = 0
    ans2 = 0

    for xx, yy in array.grid:
        if array.loc(xx, yy) == "X":
            down = [array.loc(xx, yy + i) for i in range(4)]
            up = [array.loc(xx, yy - i) for i in range(4)]
            left = [array.loc(xx - i, yy) for i in range(4)]
            right = [array.loc(xx + i, yy) for i in range(4)]
            diag_down_left = [array.loc(xx - i, yy + i) for i in range(4)]
            diag_down_right = [array.loc(xx + i, yy + i) for i in range(4)]
            diag_up_left = [array.loc(xx - i, yy - i) for i in range(4)]
            diag_up_right = [array.loc(xx + i, yy - i) for i in range(4)]
            dirs = [
                up,
                down,
                left,
                right,
                diag_down_left,
                diag_down_right,
                diag_up_left,
                diag_up_right,
            ]
            for _dir in dirs:
                if "".join(_dir) == "XMAS":
                    ans1 += 1

    key = set("MS")
    for xx, yy in array.grid:
        if array.loc(xx, yy) == "A":
            diag1 = set([array.loc(xx - 1, yy - 1), array.loc(xx + 1, yy + 1)])
            diag2 = set([array.loc(xx - 1, yy + 1), array.loc(xx + 1, yy - 1)])
            if diag1 == key and diag2 == key:
                ans2 += 1

    # array.pprint()
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

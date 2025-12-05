import sys
from lib.datastructures import Array


ROLL = "@"
EMPTY = "."


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line) for line in fp.read().splitlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    array = Array(data=data)

    ans1 = 0
    ans2 = 0

    removed = set()
    total_removed = 0
    _iter = 1

    while True:
        for ii, jj in array.grid:
            if (
                array.loc(ii, jj) == ROLL
                and sum(
                    array.loc(xx, yy) == ROLL
                    for xx, yy in array.neighbourhood(ii, jj)
                )
                < 4
            ):
                if _iter == 1:
                    ans1 += 1
                ans2 += 1
                removed.add((ii, jj))
        for ii, jj in removed:
            array.set(ii, jj, EMPTY)

        if len(removed) == total_removed:  # No rolls can be removed
            break
        total_removed = len(removed)
        _iter += 1

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

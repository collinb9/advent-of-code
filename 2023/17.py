import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, line.replace("\n", ""))) for line in fp.readlines()]

    return data


def main(fpath):
    data = Array(read_data(fpath))
    data.pprint()
    return 0, 0


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

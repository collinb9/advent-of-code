import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line.replace("\n", "")) for line in fp.readlines()]

    return data


def issymbol(string):
    return not string.isnumeric() and string != "."


def main(fpath):
    data = Array(read_data(fpath))
    numbers = []
    gears = {}
    for yy, row in enumerate(data.data):
        number = ""
        # Keep state on whether the current number is next to a symbol
        keepnumber = False
        # Keep track of the gears that are adjacent to a given number
        gears_set = set()
        for xx, value in enumerate(row):
            if value.isnumeric():
                # Still a string
                number = number + value
                for ii, jj in data.neighbourhood(xx, yy):
                    item = data.loc(ii, jj)
                    if issymbol(item):
                        if item == "*":
                            gears_set.add((ii, jj))
                        keepnumber = True
            else:
                if number.isnumeric() and keepnumber:
                    numbers.append(int(number))
                    for gear in gears_set:
                        gears.setdefault(gear, []).append(int(number))
                # Need to reset everything when we finish checking a number
                gears_set = set()
                keepnumber = False
                number = ""
        # Handling when we hit the end of a row
        if keepnumber:
            numbers.append(int(number))

    ans2 = []
    for gear, nums in gears.items():
        if len(nums) == 2:
            ans2.append(nums[0] * nums[1])

    return sum(numbers), sum(ans2)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

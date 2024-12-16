import sys
from lib.utils import ints
import math
import collections
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()

    inner = []
    outer = []

    for line in data:
        if line:
            inner.append(line)
        else:
            outer.append(inner)
            inner = []

    outer.append(inner)
    return outer


def find_integer_solution(prize_coords, a_coords, b_coords):
    "Solve system of 2 linear equations with 2 variables using matrix inversion."
    det = a_coords[0] * b_coords[1] - a_coords[1] * b_coords[0]
    if det == 0:
        return 0
    a_push, b_push = (
        prize_coords[0] * b_coords[1] - prize_coords[1] * b_coords[0]
    ) / det, (
        a_coords[0] * prize_coords[1] - a_coords[1] * prize_coords[0]
    ) / det
    if (
        a_push * 10 % 10 == 0 and b_push * 10 % 10 == 0
    ):  # Check if it is a positive integer solution
        res = a_push * 3 + b_push
    else:
        return 0
    return int(res)


def main(fpath):
    data = read_data(fpath)
    # print(data)

    ans1 = 0
    ans2 = 0

    inc = 10000000000000
    for line in data:
        *buttons, prize = line
        prize_coords = tuple(ints(prize))
        button_a, button_b = buttons
        a_coords = tuple(ints(button_a))
        b_coords = tuple(ints(button_b))

        ans1 += find_integer_solution(prize_coords, a_coords, b_coords)

        ans2 += find_integer_solution(
            (prize_coords[0] + inc, prize_coords[1] + inc), a_coords, b_coords
        )

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

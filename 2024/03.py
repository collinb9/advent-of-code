import sys
import re
import os
from lib.utils import ints


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    ans1 = 0
    ans2 = 0
    expression = r"mul\(\d{1,3},\d{1,3}\)"
    for line in data:
        res = list(map(str, re.findall(expression, line)))
        for expr in res:
            ll, rr = ints(expr)
            ans1 += ll * rr

    do = True
    expression = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    for line in data:
        res = list(map(str, re.findall(expression, line)))
        for expr in res:
            if expr.startswith("do("):
                do = True
            elif expr.startswith("don't"):
                do = False
            else:
                if do:
                    ll, rr = ints(expr)
                    ans2 += ll * rr

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

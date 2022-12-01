import sys
import math
import functools
import itertools
import collections


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.strip() for line in fp.readlines()][0]
    data = [
        list(map(int, coord.split("=")[1].split("..")))
        for coord in "".join(data.split(":")[1:]).strip().split(", ")
    ]

    return data


def x(t, v0):
    coeff = min(t, v0)
    return coeff * abs(v0) - coeff * (coeff - 1)/2 * v0 / abs(v0)


def y(t, v0):
    return t * v0 - (t-1) * t/2

def solve_for_t(y, v0):
    return (2 * v0 + 1 + math.sqrt(4 * (v0 ** 2) + 4 * v0 + 1 - 8 * y)) / 2

def maximise_y(v0):
    t = v0
    return y(t, v0)



def main(fpath):
    data = read_data(fpath)
    (x0, x1), (y1, y0) = data[0], data[1]
    vy = y1
    max_ys = []
    t = math.ceil(solve_for_t(y0, vy))
    valid_coords = set()
    while  t <= x1:
        check_0 = False
        if vy == 0:
            check_0 = True
        if y1 <= y(t, vy) <= y0:
            max_ys.append(maximise_y(vy))
            for vx in range(1, x1 + 1):
                if x0 <= x(t, vx) <= x1:
                    valid_coords.add((vx, vy))
        if y1 <= y(t+1, vy) <= y0:
            t += 1
        else:
            vy += 1
            t = math.ceil(solve_for_t(y0, vy))
    return max(max_ys), len(valid_coords)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)

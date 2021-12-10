import os
import sys
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, list(line.strip()))) for line in fp.readlines()]
    return data


def find_basin(data: Array, point, value, basin):
    for coord in data.find_adjacent(point[0], point[1]):
        v = data.find_value(coord)
        if v > value and v < 9:
            if coord not in basin:
                basin.append(coord)
            find_basin(data, coord, v, basin)


def main(fpath):
    data = Array(read_data(fpath))
    low_points = []
    low_points_loc = []
    # Part 1
    for j, i in data.grid:
        num = data.loc(i, j)
        adj_vals = [data.find_value(ll) for ll in data.find_adjacent(i, j)]
        if num < min(adj_vals):
            low_points.append(num)
            low_points_loc.append((i, j))

    # Part 2
    basins = []
    for p, v in zip(low_points_loc, low_points):
        basin = [p]
        find_basin(data, p, v, basin)
        basins.append(basin)
    return sum([n + 1 for n in low_points]), math.prod(
        map(len, sorted(basins, key=len)[-3:])
    )


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)

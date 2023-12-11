import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array
from lib.metrics import manhattan

from itertools import combinations


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line.replace("\n", "")) for line in fp.readlines()]

    return data

def expand(data):
    # Expand
    columns_to_expand = []
    rows_to_expand = []
    for i, row in enumerate( data.data ):
        if all(item  == "." for item in row):
            rows_to_expand.append(i)

    for i, column in enumerate( data.columns ):
        if all(data.loc(*item)  == "." for item in column):
            columns_to_expand.append(i)

    return rows_to_expand, columns_to_expand

def get_sum_of_distances(data, rows_to_expand, columns_to_expand, expansion_size = 1):
    # Find galaxies
    galaxies = []
    for x, y in data.grid:
        if data.loc(x, y) == "#":
            galaxies.append((x, y))

    # Get distances betwen each pair of galaxies
    res = 0
    for gal1, gal2 in combinations(galaxies, 2):
        res += manhattan(gal1, gal2)
        for row_index in rows_to_expand:
            if min(gal1[1], gal2[1]) < row_index < max(gal1[1], gal2[1]):
                res += expansion_size
        for column_index in columns_to_expand:
            if min(gal1[0], gal2[0]) < column_index < max(gal1[0], gal2[0]):
                res += expansion_size
    return res

def main(fpath):
    data = Array(read_data(fpath))

    rows_to_expand, columns_to_expand = expand(data)

    ans1 = get_sum_of_distances(data, rows_to_expand, columns_to_expand)
    ans2 = get_sum_of_distances(data, rows_to_expand, columns_to_expand, expansion_size=1_000_000 - 1)
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

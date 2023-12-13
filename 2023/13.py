import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array

def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    inner = []
    outer = []

    for line in data:
        if not line:
            outer.append(Array(inner))
            inner = []
            continue
        inner.append(line)
    outer.append(Array(inner))

    return outer


def compare_array(arr1, arr2):
    res = 0
    for xx, yy in zip(arr1, arr2):
        if xx != yy:
            res += 1
    return res


def check_rows(block):
    res = 0
    res2 = 0
    for row_index in range(block.y - 1):  # Check all rows. Go top -> bottom
        window = min(block.y - row_index - 1, row_index + 1)
        _cmp_array = [
            compare_array(block.data[row_index - xx], block.data[row_index + xx + 1])
            for xx in range(window)
        ]
        if all(item == 0 for item in _cmp_array):
            res += 100 * (row_index + 1)
        if sum(_cmp_array) == 1:
            res2 += 100 * (row_index + 1)
    return res, res2


def check_columns(block):
    res = 0
    res2 = 0
    for column_index in range(block.x - 1):  # Check all the columns. Go left -> right
        window = min(block.x - column_index - 1, column_index + 1)
        _cmp_array = [
            compare_array(
                "".join(
                    [
                        block.loc(*coord)
                        for coord in block.find_column(column_index - yy)
                    ]
                ),
                "".join(
                    [
                        block.loc(*coord)
                        for coord in block.find_column(column_index + yy + 1)
                    ]
                ),
            )
            for yy in range(window)
        ]
        if all(item == 0 for item in _cmp_array):
            res += column_index + 1
        if sum(_cmp_array) == 1:
            res2 += column_index + 1
    return res, res2


def main(fpath):
    data = read_data(fpath)

    ans1 = 0
    ans2 = 0
    for block in data:
        _row_count1, _row_count2  = check_rows(block)
        _column_count1, _column_count2  = check_columns(block)
        ans1 += _row_count1 + _column_count1
        ans2 += _row_count2 + _column_count2

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

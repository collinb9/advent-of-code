import sys
import itertools
import functools
import operator

OPERATIONS = {"+": operator.add, "*": operator.mul}


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()
    size = len(data)
    values = []
    current = ["" for _ in range(size - 1)]
    operations = []
    for i, col in enumerate(zip(*data)):
        col = list(col)
        if all(entry == " " for entry in col):
            values.append(current)
            current = ["" for _ in range(size - 1)]
            continue
        operation = col.pop()
        for i, entry in enumerate(col):
            current[i] = current[i] + entry
        if operation in OPERATIONS:
            operations.append(operation)

    values.append(current)

    return values, operations


def reararrange(nums):
    res = []
    for digits in zip(*nums):
        res.append("".join(digits))

    return res


def main(fpath):
    values, operations = read_data(fpath)

    ans1 = 0
    ans2 = 0
    for nums, operation in zip(values, operations):
        operation = OPERATIONS[operation]
        ans1 += functools.reduce(operation, map(int, nums))
        nums = reararrange(nums)
        ans2 += functools.reduce(operation, map(int, nums))

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

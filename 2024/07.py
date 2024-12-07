import sys
from operator import mul, add
import itertools


def concat(a, b):
    return int(str(a) + str(b))


OPERATORS_1 = [mul, add]
OPERATORS_2 = [mul, add, concat]


def read_data(fpath):
    data = {}
    with open(fpath, "r") as fp:
        for line in fp.readlines():
            line = line.replace("\n", "")
            result, nums = line.split(":")
            result = int(result)
            nums = list(map(int, nums.strip().split(" ")))
            data[result] = nums

    return data


def calculate_calibration(data, operators):
    res = 0
    for value, nums in data.items():
        for operator_perm in itertools.product(
            operators, repeat=len(nums) - 1
        ):
            result = nums[0]
            for num, operator in zip(nums[1:], operator_perm):
                result = operator(result, num)
            if result == int(value):
                res += value
                break
    return res


def main(fpath):
    data = read_data(fpath)

    ans1 = calculate_calibration(data, OPERATORS_1)
    ans2 = calculate_calibration(data, OPERATORS_2)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

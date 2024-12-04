import sys
import re


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [
            list(map(int, line.replace("\n", "").split()))
            for line in fp.readlines()
        ]

    return data


def is_safe(report):
    original_report = report
    current, *report = report
    diff = 0
    for index, ii in enumerate(report):
        new_diff = ii - current
        if abs(new_diff) > 3 or abs(new_diff) < 1:
            return False, index
        if new_diff * diff < 0:
            return False
        current = ii
        diff = new_diff
    return True, 0


def main(fpath):
    data = read_data(fpath)
    ans1 = 0
    ans2 = 0

    for report in data:
        val = is_safe(report)
        if val:
            ans1 += 1
            ans2 += 1
        else:
            for i in range(len(report)):
                val = is_safe(report[:i] + report[i + 1 :])
                if val:
                    ans2 += 1
                    break
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

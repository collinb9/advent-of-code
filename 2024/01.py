import sys
import re


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split() for line in fp.readlines()]

    left = []
    right = []
    for ii, jj in data:
        left.append(int(ii))
        right.append(int(jj))

    return left, right


def main(fpath):
    left, right = read_data(fpath)

    left.sort()
    right.sort()

    ans1 = sum(abs(ii - jj) for ii, jj in zip(left, right))

    counts = dict()
    for jj in right:
        if jj in counts:
            counts[jj] += 1
        else:
            counts[jj] = 1

    ans2 = sum(ii * counts.get(ii, 0) for ii in left)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

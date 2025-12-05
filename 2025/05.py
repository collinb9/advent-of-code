import sys
from lib.utils import merge_intervals


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()

    outer = []
    inner = []
    for line in data:
        if not line:
            outer.append(inner)
            inner = []
            continue
        inner.append(line)
    outer.append(inner)
    ranges, ids = outer
    ranges = [tuple(map(int, _range.split("-"))) for _range in ranges]
    ids = list(map(int, ids))
    return ranges, ids


def main(fpath):
    ranges, ids = read_data(fpath)
    ranges = merge_intervals(*ranges)

    ans1 = 0
    ans2 = 0

    for _id in ids:
        for start, end in ranges:
            if start <= _id <= end:
                ans1 += 1

    for start, end in ranges:
        ans2 += end - start + 1

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

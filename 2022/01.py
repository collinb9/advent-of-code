import sys
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]
    outer = []
    inner = []
    for dat in data:
        if dat:
            inner.append(int(dat))
        else:
            outer.append(inner)
            inner = []
    return outer



def main(fpath):
    data = read_data(fpath)
    sums = [sum(item) for item in data]
    ordered_sums = sorted(sums, reverse=True)
    return max(sums), sum(ordered_sums[:3])


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)


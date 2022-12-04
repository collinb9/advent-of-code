import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [
            [
                list(map(int, item.split("-")))
                for item in line.replace("\n", "").strip().split(",")
            ]
            for line in fp.readlines()
        ]
    return data


def fully_overlap(pair_1, pair_2):
    res = sorted(pair_1 + pair_2)
    res = [res[0], res[-1]]
    return res == pair_1 or res == pair_2


def any_overlap(pair_1, pair_2):
    res = sorted(pair_1 + pair_2)
    cond = res[0:2] != pair_1 and res[0:2] != pair_2
    return cond or (not cond and res[1] == res[2])


def main(fpath):
    data = read_data(fpath)
    j = 0
    # Part 1
    i = sum(map(lambda pair: fully_overlap(pair[0], pair[1]), data))
    # Part 2
    j = sum(map(lambda pair: any_overlap(pair[0], pair[1]), data))

    return i, j


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

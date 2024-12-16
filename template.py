import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line for line in fp.read().splitlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    print(data)

    ans1 = 0
    ans2 = 0

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

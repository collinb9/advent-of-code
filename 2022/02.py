import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [
            line.replace("\n", "")
            .replace("A", "0")
            .replace("B", "1")
            .replace("C", "2")
            .replace("X", "0")
            .replace("Y", "1")
            .replace("Z", "2")
            .split(" ")
            for line in fp.readlines()
        ]

    opp = [int(x[0]) for x in data]
    me = [int(x[1]) for x in data]
    return opp, me


def main(fpath):
    opp, me = read_data(fpath)
    i = 0
    j = 0
    for oo, mm in zip(opp, me):
        # Part 1
        i += mm + 1
        result = (mm - oo) % 3
        i += ((result + 1) % 3) * 3

        # Part 2
        desired_result = mm
        j += desired_result * 3
        inc = (oo + (desired_result + 2) % 3) % 3
        # Need to increment to match values from question
        inc += 1
        j += inc
    return i, j


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

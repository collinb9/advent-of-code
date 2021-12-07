import sys


def problem_1(fpath):
    x = 0
    y = 0
    with open(fpath, "r") as fh:
        for line in fh:
            (direction, val) = line.strip().split()
            val = int(val)
            if direction == "forward":
                x += val
            elif direction == "down":
                y += val
            elif direction == "up":
                y -= val
    print("Answer 1: ", x * y)


def problem_2(fpath):
    x = 0
    y = 0
    aim = 0
    with open(fpath, "r") as fh:
        for line in fh:
            (direction, val) = line.strip().split()
            val = int(val)
            if direction == "forward":
                x += val
                y = y + aim * val
            elif direction == "down":
                aim += val
            elif direction == "up":
                aim -= val
    print("Answer 2: ", x * y)


if __name__ == "__main__":
    fpath = sys.argv[1]
    problem_1(fpath)
    problem_2(fpath)

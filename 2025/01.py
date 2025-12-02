import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line for line in fp.read().splitlines()]

    return data


def main(fpath):
    data = read_data(fpath)

    curr = 50

    ans1 = 0
    ans2 = 0
    for line in data:
        _dir, val = line[0], line[1:]
        val = int(val)
        if _dir == "L":
            val = val * -1

        if val <= (-1 * curr): # in case val < 0:
            inc = 1 + ((val * -1) - curr) // 100
            if curr == 0:
                inc -= 1
            ans2 += inc
        elif val >= 100 - curr: # in case val > 0:
            inc = 1 + (val - (100-curr)) // 100
            ans2 += inc

        curr = (curr + val) % 100
        if curr == 0:
            ans1 += 1

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

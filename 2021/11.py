import sys
import collections
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, list(line.strip()))) for line in fp.readlines()]
    return data


def neighbourhood(data, i, j):
    x = len(data[0])
    y = len(data)
    loc = {
        (i, min(j + 1, y - 1)),
        (i, max(0, j - 1)),
        (max(0, i - 1), max(0, j - 1)),
        (max(0, i - 1), j),
        (max(0, i - 1), min(j + 1, y - 1)),
        (min(i + 1, x - 1), max(0, j - 1)),
        (min(i + 1, x - 1), j),
        (min(i + 1, x - 1), min(j + 1, y - 1)),
    }
    return [ll for ll in loc if ll != (i, j)]


def main(fpath, steps):
    data = read_data(fpath)
    no_flashes = 0
    flashed = collections.deque()
    seen = set()
    simul = 0
    step = 0
    while step < steps or simul == 0:

        # Problem 1
        for (i, j) in itertools.product(range(len(data[0])), range(len(data))):
            data[j][i] += 1
            if data[j][i] > 9:
                data[j][i] = 0
                flashed.appendleft((i, j))
                seen.add((i, j))
                no_flashes += 1
        while len(flashed) > 0:
            (ii, jj) = flashed.pop()
            for (nn, mm) in neighbourhood(data, ii, jj):
                if (nn, mm) not in seen:
                    data[mm][nn] += 1
                    if data[mm][nn] > 9:
                        data[mm][nn] = 0
                        flashed.appendleft((nn, mm))
                        seen.add((nn, mm))
                        no_flashes += 1
        step += 1
        if step == steps:
            flashes_answer = no_flashes

        # Problem 2
        if len(seen) == (len(data[0]) * len(data)):
            simul = step

        seen.clear()

    return flashes_answer, simul


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath, 100)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)

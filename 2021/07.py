import sys
import collections


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = list(map(int, fp.read().split(",")))
    return data


def problem_1(fpath):
    data = read_data(fpath)
    counter = collections.Counter(data)
    distance = 0
    for item in set(data):
        d = sum([c * abs(item - v) for v, c in counter.items()])
        if d < distance or distance == 0:
            distance = d
        else:
            break
    return distance


def problem_2(fpath):
    data = read_data(fpath)
    counter = collections.Counter(data)
    distance = 0
    for item in range(max(data)):
        d = sum(
            [c * sum(range(abs(item - v) + 1)) for v, c in counter.items()]
        )
        if d < distance or distance == 0:
            distance = d
        else:
            break
    return distance


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = problem_1(fpath)
    print("Answer 1: ", answer_1)
    answer_2 = problem_2(fpath)
    print("Answer 2: ", answer_2)

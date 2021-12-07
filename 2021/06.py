import sys
import functools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = list(map(int, fp.read().split(",")))
        # data = [int(num) for num in data]
    return data


@functools.lru_cache(maxsize=None)
def b(t, x0):
    """Babies"""
    if t < 0:
        return 0
    elif t <= x0:
        return 1
    elif t <= x0 + 7:
        return 1
    else:
        return a(t - 7, x0) + b(t - 7, x0)


@functools.lru_cache(maxsize=None)
def a(t, x0):
    """Adults"""
    if t <= x0:
        return 0
    elif t <= x0 + 9:
        return 1
    return b(t - 9, x0) + a(t - 9, x0)


def main(fpath, days=80):
    data = read_data(fpath)
    answer = 0
    for num in data:
        res = a(days, num) + b(days, num)
        answer += res

    return answer


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = main(fpath, 80)
    print("Answer 1: ", answer_1)
    answer_2 = main(fpath, 256)
    print("Answer 2: ", answer_2)

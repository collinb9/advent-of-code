import sys


def rolling_sum(data, window):
    rolling_sum = []
    for i in range(0, len(data) + 1 - window):
        rolling_window = data[i : i + window]
        rolling_sum.append(sum(rolling_window))
    return rolling_sum


def main(fpath, window=1):
    with open(fpath, "r") as fh:
        data = [int(line) for line in fh.readlines()]
    first = rolling_sum(data[1:], window=window)
    second = rolling_sum(data[:-1], window=window)
    answer = sum([int(item1 > item2) for item1, item2 in zip(first, second)])
    return answer


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = main(fpath, 1)
    print("Answer 1: ", answer_1)
    answer_2 = main(fpath, 2)
    print("Answer 2: ", answer_2)

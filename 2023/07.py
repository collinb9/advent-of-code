import sys
import collections
import functools
import operator


def read_data(path):
    with open(path, "r") as fp:
        data = [
            [collections.defaultdict(int)] + line.replace("\n", "").split()
            for line in fp.readlines()
        ]

    return data


def compare(chars, left, right):
    """If left is bigger, return 1, if right is bigger, return -1"""
    left_counts = sorted(left[0].values())
    right_counts = sorted(right[0].values())
    for _ in range(2):
        ll = left_counts.pop()
        rr = right_counts.pop()
        if ll > rr:
            return 1
        if rr > ll:
            return -1
    for ll, rr in zip(left[1], right[1]):
        if chars.index(ll) > chars.index(rr):
            return 1
        if chars.index(rr) > chars.index(ll):
            return -1

    return 0


def main(path):
    data = read_data(path)
    for line in data:
        for char in line[1]:
            line[0][char] += 1

    # Part 1
    chars1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    data = sorted(data, key=functools.cmp_to_key(functools.partial(compare, chars1)))

    ans1 = 0
    for i, line in enumerate(data, 1):
        ans1 += i * int(line[-1])

    # Part 2
    chars2 = ["J", "1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
    for line in data:
        _count = line[0]["J"]
        line[0]["J"] = 0
        _char = max(line[0].items(), key=operator.itemgetter(1))
        if _count > 0:
            if _char[0] == "J":  # Handle the case of all Js
                line[0][chars2[-1]] = len(line[1])
                continue
            line[0][_char[0]] += _count

    data = sorted(data, key=functools.cmp_to_key(functools.partial(compare, chars2)))

    ans2 = 0
    for i, line in enumerate(data, 1):
        ans2 += i * int(line[-1])

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").strip() for line in fp.readlines()]

    return data


def calculate_priority(item):
    if item.isupper():
        inc = ord(item) - ord("A") + 27
    else:
        inc = ord(item) - ord("a") + 1
    return inc


def main(fpath):
    data = read_data(fpath)
    i = 0
    k = 0
    group = []
    for j, item in enumerate(data):
        # Part 1
        slicer = int(len(item) / 2)
        first = set(item[:slicer])
        second = set(item[slicer:])
        both = first.intersection(second).pop()
        inc = calculate_priority(both)
        i += inc

        # Part 2
        group.append(set(item))
        if j % 3 == 2:
            identifier = set.intersection(group[0], group[1], group[2]).pop()
            inc = calculate_priority(identifier)
            k += inc
            group = []

    return i, k


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

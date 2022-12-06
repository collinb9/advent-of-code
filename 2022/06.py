import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().strip()

    return data


def find_marker(data, size):
    for i in range(len(data)):
        if len(set(data[i : i + size])) == size:
            return i + size


def main(fpath):
    data = read_data(fpath)
    return find_marker(data, 4), find_marker(data, 14)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

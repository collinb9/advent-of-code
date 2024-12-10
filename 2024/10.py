import sys
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, line)) for line in fp.read().splitlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    array = Array(data)

    ans1 = 0
    ans2 = 0
    # Start at height zero
    starts = set()
    for ii, jj in array.grid:
        val = array.loc(ii, jj)
        if val == 0:
            starts.add((ii, jj))

    # DFS
    for start in starts:
        destinations = set()
        full_paths = set()
        stack = []
        stack.append((start, array.loc(*start), [start]))
        while stack:
            location, value, path = stack.pop(-1)
            if value == 9:
                if location not in destinations:
                    ans1 += 1
                full_path = "".join(str(item) for item in path)
                if full_path not in full_paths:
                    ans2 += 1
                full_paths.add(full_path)
                destinations.add(location)
                continue
            for ii, jj in array.find_adjacent(*location):
                _value = array.loc(ii, jj)
                if _value - value == 1:
                    stack.append(((ii, jj), _value, path + [(ii, jj)]))

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

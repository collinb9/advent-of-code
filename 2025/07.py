import sys
import functools

START = "S"
SPLITTER = "^"

def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()

    return data


def main(fpath):
    data = read_data(fpath)

    # Find start and splitters
    rows = len(data)
    splitters = set()
    start = None
    for jj, row in enumerate(data):
        for ii, val in enumerate(row):
            if val == SPLITTER:
                splitters.add((ii, jj))
            elif val == START:
                start = (ii, jj)

    seen = set()
    ans1 = 0

    # Recursive DFS
    @functools.lru_cache
    def timelines(node):
        nonlocal ans1
        ii, jj = node
        if jj + 1 == rows:
            return 1
        if (ii, jj + 1) in splitters:
            if (ii, jj+1) not in seen:
                ans1 += 1
                seen.add((ii, jj+1))
            return timelines((ii - 1, jj + 1)) + timelines((ii + 1, jj + 1))
        return timelines((ii, jj + 1))

    ans2 = timelines(start)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

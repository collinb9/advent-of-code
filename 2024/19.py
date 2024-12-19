import sys
import functools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()
    inner = []
    outer = []

    for line in data:
        if not line:
            outer.append(inner)
            inner = []
            continue
        inner.append(line)
    outer.append(inner)

    return outer


def is_possible(patterns, max_len, design):
    design_len = len(design)
    max_len = min(design_len, max_len)

    @functools.lru_cache(maxsize=None)
    def inner(start, end):
        design_part = design[start:end]
        if design_part in patterns:
            if end == design_len:
                return 1
            return sum(
                inner(end, ii)
                for ii in range(
                    end + 1, min(end + max_len + 1, design_len + 1)
                )
            )
        return 0

    return sum(inner(0, ii) for ii in range(1, max_len + 1))


def main(fpath):
    patterns, designs = read_data(fpath)
    patterns = set(patterns[0].split(", "))
    max_len = max(len(pattern) for pattern in patterns)

    ans1 = 0
    ans2 = 0
    for design in designs:
        res = is_possible(patterns, max_len, design)
        if res > 0:
            ans1 += 1
        ans2 += res

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

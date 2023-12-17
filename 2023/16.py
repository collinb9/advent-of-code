import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array
import functools

sys.setrecursionlimit(10_000)


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line.replace("\n", "")) for line in fp.readlines()]

    return data


OUT_DIRECTION = {
    (Array.right, "-"): [Array.right],
    (Array.left, "-"): [Array.left],
    (Array.down, "-"): [Array.left, Array.right],
    (Array.up, "-"): [Array.left, Array.right],
    (Array.right, "|"): [Array.up, Array.down],
    (Array.left, "|"): [Array.up, Array.down],
    (Array.down, "|"): [Array.down],
    (Array.up, "|"): [Array.up],
    (Array.right, "\\"): [Array.down],
    (Array.left, "\\"): [Array.up],
    (Array.down, "\\"): [Array.right],
    (Array.up, "\\"): [Array.left],
    (Array.right, "/"): [Array.up],
    (Array.left, "/"): [Array.down],
    (Array.down, "/"): [Array.left],
    (Array.up, "/"): [Array.right],
}


@functools.lru_cache(maxsize=None)
def beam(point, direction):
    seen = set()

    def inner(point, direction):
        nonlocal seen
        value = data.loc(*point)
        seen.add((point, direction))

        count = set()
        count.add(point)
        _cont = False

        new_directions = OUT_DIRECTION.get((direction, value), [direction])
        for new_direction in new_directions:
            new_point = (point[0] + new_direction[0], point[1] + new_direction[1])
            if new_point in data:
                _cont = True
                if (new_point, new_direction) not in seen:
                    count = count | inner(new_point, new_direction)
        return count

    return len(inner(point, direction))


def main(fpath):
    global data
    data = Array(read_data(fpath))

    ans1 = beam((0, 0), Array.right)

    ans2 = 0
    for top in range(data.x):  # Go along top
        _res = beam((top, 0), Array.down)
        if _res > ans2:
            ans2 = _res
    for bottom in range(data.x):  # Go along bottom
        _res = beam((bottom, data.y - 1), Array.up)
        if _res > ans2:
            ans2 = _res
    for left in range(data.y):  # Go along left
        _res = beam((0, left), Array.right)
        if _res > ans2:
            ans2 = _res
    for right in range(data.y):  # Go along right
        _res = beam((data.x - 1, right), Array.left)
        if _res > ans2:
            ans2 = _res

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

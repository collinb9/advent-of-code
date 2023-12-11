import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array

import collections

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
HORIZONTAL = "H"
VERTICAL = "V"
DIRECTION_TO_ORIENTATION = {
    UP: VERTICAL,
    DOWN: VERTICAL,
    LEFT: HORIZONTAL,
    RIGHT: HORIZONTAL,
}

OPPOSITE_ORIENTATION = {VERTICAL: HORIZONTAL, HORIZONTAL: VERTICAL}

ORIENTATION_TO_DIRECTIONS = {HORIZONTAL: [LEFT, RIGHT], VERTICAL: [DOWN, UP]}


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line.replace("\n", "")) for line in fp.readlines()]

    return data


OUT_DIRECTION = {
    (RIGHT, "-"): RIGHT,
    (RIGHT, "J"): UP,
    (RIGHT, "7"): DOWN,
    (LEFT, "-"): LEFT,
    (LEFT, "L"): UP,
    (LEFT, "F"): DOWN,
    (DOWN, "|"): DOWN,
    (DOWN, "J"): LEFT,
    (DOWN, "L"): RIGHT,
    (UP, "|"): UP,
    (UP, "7"): LEFT,
    (UP, "F"): RIGHT,
}


def in_loop(point, data, loop):
    direction = LEFT # Only necessary to scan in 1 direction
    counts = [collections.defaultdict(int), collections.defaultdict(int)]
    _point = point
    count = 0
    while True:
        _point = (_point[0] + direction[0], _point[1] + direction[1])
        if _point in loop:
            _value = data.loc(*_point)
            _dirs = loop[_point]
            if (
                len(set(_dirs)) == 1
                and DIRECTION_TO_ORIENTATION[_dirs[0]]
                != DIRECTION_TO_ORIENTATION[direction]
            ):
                count += 1 # If we hit a "|"
            elif len(set(_dirs)) > 1:
                for i, _dir in enumerate(_dirs):
                    if (
                        DIRECTION_TO_ORIENTATION[_dir]
                        != DIRECTION_TO_ORIENTATION[direction]
                    ):
                        counts[i][_dir] += 1
        if (
            _point[0] < 0
            or _point[0] >= data.x
            or _point[1] < 0
            or _point[1] >= data.y
        ):  # Hit the edge
            _counts_directions = ORIENTATION_TO_DIRECTIONS[
                OPPOSITE_ORIENTATION[DIRECTION_TO_ORIENTATION[direction]]
            ]
            count += max(
                0,
                counts[1][_counts_directions[1]] - counts[0][_counts_directions[0]],
            )
            count += max(
                0,
                counts[1][_counts_directions[0]] - counts[0][_counts_directions[1]],
            )
            return count % 2 == 1


def main(fpath):
    data = Array(read_data(fpath))
    grid = list(data.grid)
    for xx, yy in grid:
        if data.loc(xx, yy) == "S":
            break
    start = (xx, yy)
    queue = collections.deque()
    direction = RIGHT
    queue.append((start, direction, {start: (None, direction)}))
    while len(queue) > 0:
        point, direction, loop = queue.popleft()
        next_point = (point[0] + direction[0], point[1] + direction[1])
        next_value = data.loc(*next_point)
        next_direction = OUT_DIRECTION.get((direction, next_value))
        if next_value == "S":
            loop.update({start: (direction, loop[start][1])})
            break
        if next_direction is not None:
            loop.update({next_point: (direction, next_direction)})
            queue.append((next_point, next_direction, loop))

    ans1 = int(len(loop) / 2)

    ans2 = 0
    # Can optimise this with flood fill, but the input size is small enough to do without
    for xx, yy in grid:
        if (xx, yy) in loop:
            continue
        if in_loop((xx, yy), data, loop):
            ans2 += 1

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

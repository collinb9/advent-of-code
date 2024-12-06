import sys
import re
from lib.datastructures import Array

GUARD = "^"
OBSTRUCTION = "#"
EMPTY = "."


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line.replace("\n", "")) for line in fp.readlines()]

    return data


def rotate_90(direction):
    # Turn right by 90 degrees
    # Consider as complex numbers (x, y) <-> x + yi
    # Rotation by 90 degrees is (x + yi) * i = -y + xi
    # i.e. (x, y) -> (-y, x)

    return (direction[1] * -1, direction[0])


def select_next(array, current, direction):
    # Get the next location and entry direction for that location
    # The input direction to this function is the entry direction to the current location
    _next = array.shift(direction, current)
    content = array.loc(*_next)
    if content == array.sentinel:
        return None, None
    if content == OBSTRUCTION:
        direction = rotate_90(direction)
        _next, direction = select_next(array, current, direction)
    return _next, direction


def path_find(array, start):
    seen = set()
    states = set()
    current = start
    direction = array.up
    while True:
        seen.add(current)
        _next, direction = select_next(array, current, direction)
        if _next == None:  # Reached the edge
            break
        if (current, direction) in states:
            return None  # Found a loop
        states.add(
            (current, direction)
        )  # The state is the current location and the exit direction
        current = _next
    return seen


def main(fpath):
    data = read_data(fpath)
    array = Array(data)
    array.sentinel = "~"

    ans1 = 0
    ans2 = 0

    # Find Guard
    for xx, yy in array.grid:
        if array.loc(xx, yy) == GUARD:
            start = (xx, yy)
            break

    seen = path_find(array, start)
    ans1 = len(seen)

    for ii, jj in array.grid:
        val = array.loc(ii, jj)
        if val == EMPTY:
            array.data[jj][ii] = OBSTRUCTION
            seen = path_find(array, start)
            if seen is None:
                print("Loop found with obstruction at", (ii, jj))
                ans2 += 1

            array.data[jj][ii] = EMPTY

    ans1 = len(seen)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

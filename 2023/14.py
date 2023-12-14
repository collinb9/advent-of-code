import sys
import itertools
import json


UP, DOWN, LEFT, RIGHT = "UP", "DOWN", "LEFT", "RIGHT"


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def transpose(data):
    return list(map(list, zip(*data)))


def tilt(data, _direction=UP):
    xx, yy = len(data[0]), len(data)
    res = [[0, -1] for _ in range(xx)]
    # left is the same as a transpose + up
    # right is the same as a transpose and down
    if _direction == LEFT:
        data = transpose(data)
        direction = UP
    elif _direction == RIGHT:
        data = transpose(data)
        direction = DOWN
    else:
        direction = _direction
    new_data = [["."] * xx for _ in range(yy)]

    for row, line in enumerate(data):
        for column, rock in enumerate(line):
            if rock == "O":
                res[column][0] += 1
            elif rock == "#":
                if direction == UP:
                    new_data[column] = (
                        new_data[column][: res[column][1] + 1]
                        + ["O"] * res[column][0]
                        + ["."] * (row - res[column][1] - res[column][0] - 1)
                        + ["#"]
                        + new_data[column][row + 1 :]
                    )
                elif direction == DOWN:
                    new_data[column] = (
                        new_data[column][: res[column][1] + 1]
                        + ["."] * (row - res[column][1] - res[column][0] - 1)
                        + ["O"] * res[column][0]
                        + ["#"]
                        + new_data[column][row + 1 :]
                    )
                res[column][0] = 0
                res[column][1] = row
    for column in range(xx):
        if direction == UP:
            new_data[column] = (
                new_data[column][: res[column][1] + 1]
                + ["O"] * res[column][0]
                + ["."] * (yy - 1 - res[column][1] - res[column][0])
            )
        elif direction == DOWN:
            new_data[column] = (
                new_data[column][: res[column][1] + 1]
                + ["."] * (yy - 1 - res[column][1] - res[column][0])
                + ["O"] * res[column][0]
            )

    if _direction in [UP, DOWN]:
        new_data = transpose(new_data)
    return new_data


def get_load(data):
    yy = len(data)
    ans = 0
    for row, line in enumerate(data):
        for rock in line:
            if rock == "O":
                ans += yy - row
    return ans


def main(fpath):
    data = read_data(fpath)

    # For part 2, we need to find a cycle and then use modular arithmetic
    _cycle = itertools.cycle([UP, LEFT, DOWN, RIGHT])
    iterations_to_complete = 1_000_000_000 * 4
    seen = []
    _loads = []
    for i, direction in enumerate(_cycle):
        data = tilt(data, direction)
        fingerprint = hash(direction + json.dumps(data))
        if i == 1:
            ans1 = get_load(data)
        _load = get_load(data)
        if fingerprint in seen:
            cycle_start = seen.index(fingerprint)
            _loads = _loads[cycle_start:]
            break
        _loads.append(_load)
        seen.append(fingerprint)
    iterations_left = (iterations_to_complete - cycle_start) % (i - cycle_start)
    ans2 = _loads[iterations_left - 1]

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

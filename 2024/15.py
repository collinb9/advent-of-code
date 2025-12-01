import sys
from lib.datastructures import Array
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = (list(line) for line in fp.read().splitlines())

    inner = []
    outer = []

    for line in data:
        if line:
            inner.append(line)
        else:
            outer.append(inner)
            inner = []

    outer.append(inner)
    return outer


DIRECTIONS = {
    "^": Array.up,
    "v": Array.down,
    "<": Array.left,
    ">": Array.right,
}
WALL = "#"
BOX = "O"
LEFT_BOX = "["
RIGHT_BOX = "]"
ROBOT = "@"


def simulate(array, directions, part=1):
    wall = dict()
    boxes = dict()
    for ii, jj in array.grid:
        val = array.loc(ii, jj)
        if val == ROBOT:
            start = (ii, jj)
        elif val == WALL:
            wall[(ii, jj)] = WALL
        elif val in [BOX, LEFT_BOX, RIGHT_BOX]:
            boxes[(ii, jj)] = val

    # print(boxes)

    current = start
    for direction in directions:
        _dir = DIRECTIONS[direction]
        _next = (current[0] + _dir[0], current[1] + _dir[1])
        if _next in wall:
            continue
        if _next not in boxes:
            current = _next
            continue
        # Hit a box
        # print("Hit a box")
        inc = 1
        first_box = _next

        _boxes = []
        
        # DFS to check if box is moveable

        stack = [[]]

        while True:
            loc = (_next[0] + _dir[0] * inc, _next[1] + _dir[1] * inc)
            if loc in wall:  # Can't move the box
                break
            if loc in boxes:
                inc += 1
                _boxes.append(loc)
                continue
            # print(_boxes)
            # Shift every box and move current position
            # for _box in _boxes:
            #     boxes.remove(_box)
            if len(_boxes) > 1:
                for _box1, _box2 in zip(_boxes, _boxes[1:]):
                    boxes[_box2] = boxes[_box1]
                boxes[loc] = boxes[_box2]
            else:
                boxes[loc] = boxes[first_box]
            del boxes[first_box]
            # boxes.remove(first_box)
            # boxes.add(loc)
            current = _next
            break
    return boxes, wall


def main(fpath):
    _map, directions = read_data(fpath)
    # print(map)
    # print(directions)
    directions = itertools.chain.from_iterable(directions)

    array = Array(_map)
    array.pprint()

    ans1 = 0
    ans2 = 0

    boxes, wall = simulate(array, directions, part=1)

    # tmp_array = Array.from_dict({**boxes, **wall})
    # tmp_array.pprint()

    for box in boxes:
        # print(box)
        ans1 += 100 * box[1] + box[0]

    new_data = {}
    for ii, jj in array.grid:
        val = array.loc(ii, jj)
        # if ii % 2 == 0:
        if val == WALL:
            new_data[(ii * 2 + 1, jj)] = val
        elif val == BOX:
            new_data[(ii * 2, jj)] = LEFT_BOX
            new_data[(ii * 2 + 1, jj)] = RIGHT_BOX
            continue
        new_data[(ii * 2, jj)] = val

    array = array.from_dict(new_data)
    array.pprint()

    # boxes = simulate(array, directions, part=2)
    # for box in boxes:
    #     ans2 += 100 * box[1] + box[0]

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

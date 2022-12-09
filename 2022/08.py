import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, list(line.strip()))) for line in fp.readlines()]
    return data


def main(fpath):
    data = Array(read_data(fpath))
    visible = 0
    scores = []
    for j, i in data.grid:
        num = data.loc(i, j)
        up = [data.find_value(coord) for coord in data.find_all_up(i, j)]
        down = [data.find_value(coord) for coord in data.find_all_down(i, j)]
        left = [data.find_value(coord) for coord in data.find_all_left(i, j)]
        right = [data.find_value(coord) for coord in data.find_all_right(i, j)]
        # check for edge trees
        if i == 0 or i == data.x - 1 or j == 0 or j == data.y - 1:
            visible += 1
            continue

        left_score = 0
        right_score = 0
        up_score = 0
        down_score = 0
        _visible = False
        for tree in right:
            right_score += 1
            if tree >= num:
                break
        else:
            _visible = True
        for tree in left[::-1]:
            left_score += 1
            if tree >= num:
                break
        else:
            _visible = True
        for tree in up[::-1]:
            up_score += 1
            if tree >= num:
                break
        else:
            _visible = True
        for tree in down:
            down_score += 1
            if tree >= num:
                break
        else:
            _visible = True
        score = left_score * right_score * up_score * down_score
        scores.append(score)
        if _visible:
            visible += 1

    return visible, max(scores)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

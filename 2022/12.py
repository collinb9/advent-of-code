import sys
import os
import queue
from typing import Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.datastructures import Array


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def elevation(current_char):

    if current_char == "S":
        return ord("a")
    if current_char == "E":
        return ord("z")
    return ord(current_char)


def search(
    data, start: Tuple[int], end: Tuple[int] = None, end_char: str = None
):
    """
    DFS
    """
    sentinel = data.x * data.y + 1
    distances = [[sentinel for _ in range(data.x)] for _ in range(data.y)]
    distances[start[1]][start[0]] = 0
    _queue = queue.Queue()
    _queue.put((0, start))
    while not _queue.empty():
        current_distance, current = _queue.get()
        if end_char is not None:  # Stop at first instance of a certain char
            if data.find_value(current) == end_char:
                end = current
                break
        elif current == end:  # Stop when we hit a given coordinate
            break
        _adjacent = data.find_adjacent(current[0], current[1])

        for ii, jj in _adjacent:
            if (
                elevation(data.loc(ii, jj))
                - elevation(data.find_value(current))
                >= -1
            ):
                d = current_distance + 1
                if d < distances[jj][ii]:
                    distances[jj][ii] = d
                    _queue.put((distances[jj][ii], (ii, jj)))
    total_distance = distances[end[1]][end[0]]
    return total_distance


def main(fpath):
    data = read_data(fpath)
    data = Array(data)

    # Find start and end entries
    E = False
    S = False
    for ii, jj in data.grid:
        if data.loc(ii, jj) == "S":
            start = (ii, jj)
            S = True
        if data.loc(ii, jj) == "E":
            end = (ii, jj)
            E = True
        if E and S:
            break

    # Perform DFS from end to start
    ### Part 1
    ans1 = search(data, start=end, end=start)
    ### Part 2
    ans2 = search(data, start=end, end_char="a")

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys
import os
import itertools
import queue


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lib.utils as utils


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = set(tuple(utils.ints(line)) for line in fp.readlines())
    return data


def main(fpath):
    data = read_data(fpath)

    ## Part 1
    ans1 = 0
    for x, y, z in data:
        if (x + 1, y, z) not in data:
            ans1 += 1
        if (x - 1, y, z) not in data:
            ans1 += 1
        if (x, y + 1, z) not in data:
            ans1 += 1
        if (x, y - 1, z) not in data:
            ans1 += 1
        if (x, y, z + 1) not in data:
            ans1 += 1
        if (x, y, z - 1) not in data:
            ans1 += 1

    ## Part 2

    # BFS to fill up the space with water and smoke
    xmin = min(data, key=lambda x: x[0])[0]
    xmax = max(data, key=lambda x: x[0])[0]
    ymin = min(data, key=lambda x: x[1])[1]
    ymax = max(data, key=lambda x: x[1])[1]
    zmin = min(data, key=lambda x: x[2])[2]
    zmax = max(data, key=lambda x: x[2])[2]
    _queue = queue.Queue()
    start = (xmin -1, ymin -1, zmin -1)
    _queue.put(start)
    ans2 = 0
    visited = set()
    while not _queue.empty():
        x, y, z = _queue.get()
        if x > xmax + 1 or y > ymax + 1 or z > zmax + 1 or x < xmin -1 or y < ymin - 1 or z < zmin - 1:
            continue
        for point in [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]:
            if point in data:
                ans2 += 1
            else:
                if point not in visited:
                    _queue.put(point)
                    visited.add(point)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

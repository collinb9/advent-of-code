import sys
from lib.datastructures import Array, PrioritizedItem
from lib.metrics import manhattan
import queue
import functools
import collections

EMPTY = "."
DIRECTIONS = [Array.up, Array.down, Array.left, Array.right]


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line) for line in fp.read().splitlines()]

    return data


def find_path(array: Array, start, end):
    # Dijkstra / A*
    priority_queue = queue.PriorityQueue()
    priority_queue.put(
        PrioritizedItem(priority=manhattan(start, end), item=(start, [start]))
    )
    seen = set()
    found_end = False
    while not found_end:
        if priority_queue.empty():
            raise RuntimeError("No path found")
        priority_item = priority_queue.get()
        _loc, path = priority_item.item
        seen.add(_loc)
        for _dir in DIRECTIONS:
            next_loc = array.shift(_loc, _dir)
            if next_loc == end:
                path.append(next_loc)
                found_end = True
                break
            if next_loc in seen:
                continue
            if array.loc(*next_loc) == EMPTY:
                priority_queue.put(
                    PrioritizedItem(
                        priority=(len(path) + 1 + manhattan(next_loc, end)),
                        item=(next_loc, path + [next_loc]),
                    )
                )
                continue
    return path


def count_savings(path, indexes, picos, threshold=100):
    res = 0
    for ii, _start in enumerate(path):
        for _end in path[ii + 1 :]:
            _dist = manhattan(_start, _end)
            if manhattan(_start, _end) <= picos:
                start_index, end_index = indexes[_start], indexes[_end]
                saving = end_index - start_index - _dist
                if saving >= threshold:
                    res += 1
    return res


def main(fpath):
    data = read_data(fpath)
    array = Array(data=data)
    # array.pprint()

    ans1 = 0
    ans2 = 0

    start = None
    end = None
    # Find start and end
    for ii, jj in array.grid:
        val = array.loc(ii, jj)
        if val == "S":
            start = (ii, jj)
        elif val == "E":
            end = (ii, jj)
        if start is not None and end is not None:
            break

    # Get the path

    path = find_path(array, start, end)

    indexes = {}
    for ii, loc in enumerate(path):
        indexes[loc] = ii

    ans1 = count_savings(path, indexes, picos=2, threshold=100)
    ans2 = count_savings(path, indexes, picos=20, threshold=100)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys
from lib.datastructures import AbstractArray, PrioritizedItem
from lib.metrics import manhattan
import queue

CORRUPTED = "#"
EMPTY = "."


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = []
        for item in fp.read().splitlines():
            xx, yy = item.split(",")
            data.append((int(xx), int(yy)))
    return data


def find_shortest_path(array: AbstractArray, start, end):
    # Dijkstra / A*
    directions = [array.up, array.down, array.left, array.right]
    priority_queue = queue.PriorityQueue()
    priority_queue.put(
        PrioritizedItem(priority=manhattan(start, end), item=(start, 0))
    )
    seen = set()
    found_end = False
    while not found_end:
        if priority_queue.empty():
            raise RuntimeError("No path found")
        priority_item = priority_queue.get()
        _loc, path_length = priority_item.item
        seen.add(_loc)
        for _dir in directions:
            next_loc = array.shift(_loc, _dir)
            if next_loc == end:
                path_length += 1
                found_end = True
                break
            if next_loc in seen:  # and seen[next_loc] < path_length + 1:
                continue
            if array.loc(*next_loc, empty=EMPTY) == EMPTY:
                priority_queue.put(
                    PrioritizedItem(
                        priority=(path_length + 1 + manhattan(next_loc, end)),
                        item=(next_loc, path_length + 1),
                    )
                )
                continue
    return path_length


def simulate(data, xx, yy, steps):
    start = (0, 0)
    end = (xx, yy)
    _data = parse_to_dict(data[:steps])
    array = AbstractArray(data=_data, xx=xx, yy=yy)

    res = find_shortest_path(array, start, end)
    return res


def bin_search(data, xx, yy):
    end = len(data)
    start = 0
    while True:
        if end - start == 1:
            try:
                simulate(data, xx, yy, start)
            except RuntimeError:
                print("No path found")
                return ",".join(map(str, data[start - 1]))
            return ",".join(map(str, data[end - 1]))
        mid = start + ((end - start) // 2)
        try:
            simulate(data, xx, yy, mid)
        except RuntimeError:
            end = mid
        else:
            start = mid


def parse_to_dict(data):
    _data = {}
    for x, y in data:
        _data[(x, y)] = CORRUPTED
    return _data


def main(fpath):
    data = read_data(fpath)
    xx, yy = 70, 70
    steps = 1024
    ans1 = simulate(data, xx, yy, steps)
    ans2 = bin_search(data, xx, yy)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

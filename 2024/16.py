import sys
from lib.datastructures import Array, PrioritizedItem
from lib.utils import rotate_90, rotate_270
import queue

WALL = "#"


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line) for line in fp.read().splitlines()]

    return data


def search(array, start, end):
    """
    Dijkstra
    """
    priority_queue = queue.PriorityQueue()
    priority_queue.put(
        PrioritizedItem(priority=0, item=(start, array.right, set()))
    )
    seen = dict()
    best_score = None
    best_paths = set()
    while not priority_queue.empty():
        priority_item = priority_queue.get()
        score = priority_item.priority
        pos, _dir, path = priority_item.item
        seen[(pos, _dir)] = score
        for next_pos, next_dir in [
            (array.shift(pos, _dir), _dir),
            (array.shift(pos, rotate_90(_dir)), rotate_90(_dir)),
            (array.shift(pos, rotate_270(_dir)), rotate_270(_dir)),
        ]:
            if next_dir == _dir:
                inc = 1
            else:
                inc = 1001
            if next_pos == end:
                if best_score is None:
                    best_score = score + inc
                    best_paths = path.union({next_pos})
                elif score + inc < best_score:
                    best_score = score + inc
                    best_paths = path.union({next_pos})
                elif score + inc == best_score:
                    best_paths = best_paths.union(path.union({next_pos}))
            if (
                array.loc(*next_pos) != WALL
                and (
                    (next_pos, next_dir) not in seen
                    or seen[(next_pos, next_dir)] > score + inc
                )
                and (best_score is None or score + inc <= best_score)
            ):
                priority_queue.put(
                    PrioritizedItem(
                        priority=score + inc,
                        item=(next_pos, next_dir, path.union({next_pos})),
                    )
                )
    return best_score, len(best_paths) + 1


def main(fpath):
    data = read_data(fpath)
    array = Array(data)

    ans1 = 0
    ans2 = 0

    for ii, jj in array.grid:
        val = array.loc(ii, jj)
        if val == "S":
            start = (ii, jj)
        elif val == "E":
            end = (ii, jj)

    ans1, ans2 = search(array, start, end)
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

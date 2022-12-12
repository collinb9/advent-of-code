import sys
from typing import List
import queue


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data

def adjacent(i, j, x, y):
    loc = [
        (i, min(j + 1, y - 1)),
        (i, max(0, j - 1)),
        (max(0, i - 1), j),
        (min(i + 1, x - 1), j),
    ]
    return [ll for ll in loc if ll != (i, j)]

def elevation(current_char):

    if current_char == "S":
        return ord("a")
    if current_char == "E":
        return ord("z")
    return ord(current_char)

def search(data, start, _distances: dict):
    """
    Dijkstra
    """
    xx, yy = len(data[0]), len(data)

    sentinel = xx * yy
    distances = [[sentinel for _ in range(xx)] for _ in range(yy)]
    distances[start[1]][start[0]] = 0
    priority_queue = queue.PriorityQueue()
    priority_queue.put((0, start))
    seen = set()
    while not priority_queue.empty():
        current_distance, current = priority_queue.get()
        print(current)
        if data[current[1]][current[0]] == "E":
            end = current
            print("Found end", end)
            break
        _adjacent = set(adjacent(current[0], current[1], xx, yy))
        already_seen = _distances.keys() & _adjacent
        if already_seen == _adjacent:
            min_distance = min([_distances[node] for node in already_seen])
            _distances[current] = min_distance + 1
            return current_distance + min_distance

        else:
            for (ii, jj) in _adjacent - _distances.keys():
                if elevation(data[jj][ii]) - elevation(data[current[1]][current[0]]) <= 1:
                    # if (ii, jj) not in seen:
                    d = current_distance + 1
                    if d < distances[jj][ii]:
                        # print("Inserting distance", d , "for", (ii, jj), "=", data[jj][ii], "neighbour of", current, "=", data[current[1]][current[0]])
                        distances[jj][ii] = d
                        priority_queue.put((distances[jj][ii], (ii, jj)))
        seen.add(current)
    total_distance = distances[end[1]][end[0]]
    # print(distances)
    for node in seen:
        _distances[node] = min(_distances.get(node, sentinel), total_distance - distances[node[1]][node[0]])
    return  total_distance


def main(fpath):
    data = read_data(fpath)
    xx, yy = len(data[0]), len(data)
    _distances = dict()
    # Find start
    for ii in range(xx):
        for jj in range(yy):
            if data[jj][ii] == "S":
                # data[jj][ii] = "a"
                start = (ii, jj)
                break
    ans1  = search(data, start, _distances)

    to_visit = set()
    for ii in range(xx):
        for jj in range(yy):
            if data[jj][ii] == "a":
                # data[jj][ii] = "a"
                to_visit.add((ii, jj))
    min_distance = None
    for node in to_visit:
        if node not in _distances:
            _  = search(data, start, _distances)
        # print(_distances)
    min_distance = min([v for k, v in _distances.items() if data[k[1]][k[0]] in set(["a", "S"])] + [ans1])
    return  ans1, min_distance


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

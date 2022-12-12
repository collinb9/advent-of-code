import sys
import os
import queue

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


def search(data, start, _distances: dict):
    """
    Dijkstra
    """
    sentinel = data.x * data.y
    distances = [[sentinel for _ in range(data.x)] for _ in range(data.y)]
    distances[start[1]][start[0]] = 0
    priority_queue = queue.PriorityQueue()
    priority_queue.put((0, start))
    came_from = {start: None}
    seen = set()
    while not priority_queue.empty():
        current_distance, current = priority_queue.get()
        if data.find_value(current) == "E":
            end = current
            break
        _adjacent = set(data.find_adjacent(current[0], current[1]))
        seen = seen.union(_distances.keys() & _adjacent)

        for (ii, jj) in _adjacent:
            if (
                elevation(data.loc(ii, jj))
                - elevation(data.find_value(current))
                <= 1
            ):
                d = current_distance + 1
                if d < distances[jj][ii]:
                    distances[jj][ii] = d
                    if (
                        ii,
                        jj,
                    ) not in _distances:  # Only search nodes that don't have a full path associated with them
                        priority_queue.put((distances[jj][ii], (ii, jj)))
                        came_from[(ii, jj)] = current
    try:
        total_distance = distances[end[1]][end[0]]
    except UnboundLocalError:  # Failed to reach end
        try:
            min_distance = min(
                {
                    k: v + distances[k[1]][k[0]]
                    for k, v in _distances.items()
                    if k in seen
                }.items(),
                key=lambda x: x[1],
            )
        except ValueError:  # Never reached a node which was part of a successful search
            _distances[start] = sentinel
            return sentinel
        _distances[start] = min_distance[1]
        return min_distance[1]

    # Get the path from the stating node to the end
    path = []
    current = end
    while current != start:
        prev = came_from[current]
        path.append(prev)
        current = prev
    path.append(current)
    for node in path:
        _distances[node] = min(
            _distances.get(node, sentinel),
            total_distance - distances[node[1]][node[0]],
        )
    return total_distance


def main(fpath):
    data = read_data(fpath)
    data = Array(data)
    _distances = dict()

    # Find start and 'a' entries
    to_visit = set()
    for jj, ii in data.grid:
        if data.loc(ii, jj) == "S":
            start = (ii, jj)
        if data.loc(ii, jj) == "a":
            to_visit.add((ii, jj))

    ### Part 1
    ans1 = search(data, start, _distances)

    ### Part 2
    for node in to_visit:
        if node not in _distances:
            search(data, node, _distances)
    min_distance = min([_distances[k] for k in to_visit] + [ans1])
    return ans1, min_distance


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

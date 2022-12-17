import sys
import re
import queue
import copy
import itertools


def parse_valves(s: str):
    return list(re.findall(r"\d+|[A-Z]{2}", s))


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [parse_valves(line) for line in fp.readlines()]
    valves = dict()
    for item in data:
        valves[item[0]] = (int(item[1]), item[2:])

    return valves


def released_pressure(current_time, distance, rate, end=30):
    duration = max(0, end - current_time - distance - 1)
    return rate * duration


def find_best_path(valves, distances, end):
    """
    Strategy:
    * A modified Dijkstra
    * Order by pressure relieved
    * Put in an exit condition - calculate the pressure released if you opened all valves,
      and if that value is less than the currently stored max, exit.
    """
    valves = {k: v for k, v in valves.items() if v[0] > 0}

    END = end
    _queue = queue.PriorityQueue()
    # Queue entries are (-1 * pressure_relieved, time, open_valves, path, valve)
    _queue.put((0, 0, set(), [], "AA"))
    total = 0
    final_path = []
    while not _queue.empty():
        pressure_relieved, time, open_valves, path, vv = _queue.get()
        pressure_relieved *= -1
        stop = True
        if (
            pressure_relieved
            + sum(
                [
                    released_pressure(
                        time, distances[vv][uu], valves[uu][0], end=END
                    )
                    for uu in valves.keys() - open_valves
                ]
            )
            <= total
        ):
            continue
        for uu in valves:
            if uu not in open_valves:
                distance = distances[vv][uu]
                _flow = released_pressure(
                    time, distance, valves[uu][0], end=END
                )
                if _flow > 0:
                    _open_valves = copy.copy(open_valves)
                    _open_valves.add(uu)
                    _path = copy.copy(path)
                    _path.append(uu)

                    # Multiply pressure_relieved by -1 to search highest values first
                    _next = (
                        (pressure_relieved + _flow) * -1,
                        time + distance + 1,
                        _open_valves,
                        _path,
                        uu,
                    )
                    _queue.put(_next)
                    stop = False
        if stop:
            if pressure_relieved > total:
                total = pressure_relieved
                final_path = path
    return total, final_path


def main(fpath):
    valves = read_data(fpath)
    distances = {vv: {} for vv in valves}

    sentinel = len(valves) * 2

    # Find shortes path between all pairs of points
    for vv in valves:
        for uu in valves[vv][1]:
            distances.get(vv, {})[uu] = 1
            distances.get(vv, {})[vv] = 0

    for vv in valves:
        for uu in valves:
            for ss in valves:
                distances[uu][ss] = min(
                    distances[uu].get(ss, sentinel),
                    distances[uu].get(vv, sentinel)
                    + distances[vv].get(ss, sentinel),
                )

    # Can discard all valves with a flow rate of 0
    valves = {k: v for k, v in valves.items() if v[0] > 0}

    ### Part 1

    END = 30
    ans1, _ = find_best_path(valves, distances, 30)

    ### Part 2

    # TODO: This is a horribly slow and ugly solution, want to optimise it a bit
    END = 26
    _queue = queue.PriorityQueue()
    # Queue entries are (-1 * pressure_relieved, open_valves, (time_elephant, valve_elephant), (time_me, valve_me))
    _queue.put((0, set(), [], (0, "AA"), (0, "AA")))
    total = 0
    pressure_relieved = 0
    final_path = []
    total_valves = len(valves)
    while not _queue.empty():
        (
            pressure_relieved,
            open_valves,
            path,
            elephant,
            me,
        ) = _queue.get()
        pressure_relieved *= -1
        stop = True

        min_time = min(elephant[0], me[0])
        if (
            pressure_relieved
            + sum(
                [
                    released_pressure(
                        min_time, distances[me[1]][uu], valves[uu][0], end=END
                    )
                    for uu in valves.keys() - open_valves
                ]
            )
            <= total
        ):
            continue

        for uu in valves:
            if uu not in open_valves:
                add_to_queue = False
                _pressure_relieved = pressure_relieved
                distance_elephant = distances[elephant[1]][uu]
                distance_me = distances[me[1]][uu]
                _flow_elephant = released_pressure(
                    elephant[0], distance_elephant, valves[uu][0], end=END
                )
                _flow_me = released_pressure(
                    me[0], distance_me, valves[uu][0], end=END
                )
                _open_valves = copy.copy(open_valves)
                _path = copy.copy(path)
                _next_elephant = elephant
                _next_me = me
                if _flow_elephant > 0 and elephant[0] == min_time:
                    _open_valves.add(uu)
                    _pressure_relieved += _flow_elephant
                    _next_elephant = (
                        elephant[0] + distance_elephant + 1,
                        uu,
                    )
                    stop = False
                    add_to_queue = True
                elif _flow_me > 0 and me[0] == min_time:
                    _open_valves.add(uu)
                    _pressure_relieved += _flow_me
                    _next_me = (
                        me[0] + distance_me + 1,
                        uu,
                    )
                    stop = False
                    add_to_queue = True
                if add_to_queue:
                    _path.append(
                        (
                            _pressure_relieved,
                            _flow_elephant,
                            _next_elephant,
                            _flow_me,
                            _next_me,
                        )
                    )
                    _queue.put(
                        (
                            _pressure_relieved * -1,
                            _open_valves,
                            _path,
                            _next_elephant,
                            _next_me,
                        )
                    )
        if stop:
            if pressure_relieved > total:
                total = pressure_relieved
                final_path = path

    ans2 = total

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

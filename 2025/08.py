import sys
import heapq
import collections
import functools
import operator


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [
            tuple(map(int, line.split(","))) for line in fp.read().splitlines()
        ]

    return data


def distance(p1, p2):
    return sum((x1 - x2) ** 2 for x1, x2 in zip(p1, p2))


def main(fpath):
    data = read_data(fpath)

    heap = []
    for i, p1 in enumerate(data):
        for p2 in data[i + 1 :]:
            dist = distance(p1, p2)
            heapq.heappush(heap, (dist, p1, p2))

    circuits = collections.defaultdict(set)
    connections = {}
    circuit_index = 0
    ii = 0
    while True:
        if ii == 1000:  # part 1 condition
            values = map(len, circuits.values())
            biggest_circuits = sorted(values, reverse=True)
            ans1 = functools.reduce(operator.mul, biggest_circuits[:3])
        if len(circuits) == 1 and len(connections) == len(
            data
        ):  # part 2 condition
            ans2 = p1[0] * p2[0]
            break
        ii += 1
        dist, p1, p2 = heapq.heappop(heap)
        if p1 not in connections:
            if p2 not in connections:
                # Neither p1 nor p2 are connected
                connections[p1] = circuit_index
                connections[p2] = circuit_index
                circuits[circuit_index].add(p1)
                circuits[circuit_index].add(p2)
                circuit_index += 1
                continue
            # p2 is connected, p1 is not
            circuit = connections[p2]
            connections[p1] = circuit
            circuits[circuit].add(p1)
            continue

        if p2 in connections:
            if connections[p1] == connections[p2]:
                # p1 and p2 are already connected to the same circuit
                continue
            # p1 and p2 are already connected, but to different circuits. We need to merge those circuits
            circuit_p1 = connections[p1]
            circuit_p2 = connections[p2]
            for point in circuits[circuit_p2]:
                connections[point] = circuit_p1
                circuits[circuit_p1].add(point)
            del circuits[circuit_p2]

        # p1 is connected, p2 is not
        circuit = connections[p1]
        connections[p2] = circuit
        circuits[circuit].add(p2)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

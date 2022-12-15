import sys
import re
import itertools

def ints(s: str):
    return list(map(int, re.findall(r"-?\d+", s)))

def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [ints(line) for line in fp.readlines()]

    return data

def manhattan(s, b):
    return abs(s[0] - b[0]) + abs(s[1] - b[1])

def main(fpath):
    data = read_data(fpath)
    print(data)
    sensors = set()
    beacons = set()
    for s1, s2, b1, b2 in data:
        sensor = (s1, s2)
        beacon = (b1, b2)
        sensors.add((sensor, manhattan(sensor, beacon)))
        beacons.add(beacon)

    ### Part 1

    ##  Test input
    # line = 10

    ## Real input
    line = 2_000_000

    covered = set()
    for sensor, radius in sensors:
        distance_y = abs(sensor[1] - line)
        if distance_y <= radius:
            distance_x = radius - distance_y
            intersection_point = (sensor[0], line)
            covered.add(intersection_point)
            for i in range(distance_x):
                inc = i+1
                covered.add((sensor[0] - inc, line))
                covered.add((sensor[0] + inc, line))

    no_beacons = covered - beacons

    ### Part 1

    ##  Test input
    boundary = 20

    ## Real input
    # boundary = 4_000_000

    covered = set()
    for sensor, radius in sensors:
        for i in range(radius + 1):
            sx = sensor[0]
            sy = sensor[1]
            x, y = i, radius - i
            print(sensor, radius, x, y)
            if 0 <= sx + x <= boundary and 0 <= sy + y <= boundary:
                covered.add((sx + x, sy + y))
                print("Adding", (sx + x, sy + y))
            if 0 <= sx + x <= boundary and 0 <= sy - y <= boundary:
                covered.add((sx + x, sy - y))
                print("Adding", (sx + x, sy - y))
            if 0 <= sx - x <= boundary and 0 <= sy + y <= boundary:
                covered.add((sx - x, sy + y))
                print("Adding", (sx - x, sy + y))
            if 0 <= sx - x <= boundary and 0 <= sy - y <= boundary:
                covered.add((sx - x, sy - y))
                print("Adding", (sx - x, sy - y))

    # ans = x * 4_000_000 + y


    grid = set(itertools.product(range(boundary + 1), range(boundary + 1)))
    print(len(covered))
    print(len(grid))
    print(len(grid - covered - beacons))

    return len(no_beacons), grid - covered - beacons


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

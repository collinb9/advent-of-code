import sys
import os
import re
import itertools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lib.utils as utils


def ints(s: str):
    return list(map(int, re.findall(r"-?\d+", s)))


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [ints(line) for line in fp.readlines()]

    return data


def manhattan(s, b):
    return abs(s[0] - b[0]) + abs(s[1] - b[1])


def is_point_covered(point, sensors):
    for sensor, radius in sensors:
        if manhattan(point, sensor) <= radius:
            return True
    return False


def line_intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return int(x), int(y)
    else:
        return False


def main(fpath):
    data = read_data(fpath)
    sensors = set()
    beacons = set()
    for s1, s2, b1, b2 in data:
        sensor = (s1, s2)
        beacon = (b1, b2)
        sensors.add((sensor, manhattan(sensor, beacon)))
        beacons.add(beacon)

    ##### Part 1

    # # Test input
    # line = 10

    # Real input
    line = 2_000_000

    intervals = []
    for sensor, radius in sensors:
        distance_y = abs(sensor[1] - line)
        if distance_y <= radius:  # Sensor's area intersects with the line
            distance_x = radius - distance_y
            intervals.append(
                (sensor[0] - distance_x - 1, sensor[0] + distance_x + 1)
            )

    merged_intervals = utils.merge_intervals(*intervals)
    ii = 0
    for interval in merged_intervals:
        ii += interval[1] - interval[0]

    no_beacons = ii - len([x for x in beacons if x[1] == line])

    ##### Part 2

    ## Insights
    # * The last remaining point will be a distance >= radius + 1 from every sensor, i.e. it will be at a point which is exactly radius + 1 from multiple sensors
    # * Such an intersection must necessarly be along an edge due to the shape of the locus of the manhattan distance.
    #   (It is also possible for an intersection to happen at a point, but this case is irrelevant for this problem.
    # * The point we are looking for must be at the intersection of at least 4 sensors, and this will be the intersection of two pairs of overlapping edges

    ## Strategy
    # * Find pairs of sensors which are a distance radius1 + radius2 + 2 from each other
    # * For each pair, find a point on the line which contains the common edge of those sensors detected areas
    # * Find the intersection of those two lines, and that should give us our desired point

    key_sensors = set()
    lines = set()
    points = set()
    for (sensor1, radius1), (sensor2, radius2) in itertools.combinations(
        sensors, 2
    ):
        distance = manhattan(sensor1, sensor2)
        if manhattan(sensor1, sensor2) == radius1 + radius2 + 2:

            direction = (
                int(
                    (sensor1[0] - sensor2[0])
                    / max(1, abs(sensor1[0] - sensor2[0]))
                ),
                int(
                    (sensor1[1] - sensor2[1])
                    / max(1, abs(sensor1[1] - sensor2[1]))
                ),
            )
            if direction == (1, 1):
                slope = -1
                point_on_line = (sensor1[0] - radius1 - 1, sensor1[1])
            elif direction == (1, -1):
                slope = 1
                point_on_line = (sensor1[0] - radius1 - 1, sensor1[1])
            elif direction == (-1, 1):
                slope = 1
                point_on_line = (sensor1[0] - radius1 - 1, sensor1[1])
            elif direction == (-1, -1):
                slope = -1
                point_on_line = (sensor1[0] + radius1 + 1, sensor1[1])
            else:
                point = (
                    sensor2[0] + direction[0] * (radius2 + 1),
                    sensor2[0] + direction[0] * (radius2 + 1),
                )
                key_sensors.add(((sensor1, radius1), (sensor2, radius2)))
                points.add(point)
                continue

            # line = [a, b, c] <==> a * x + b * y = c
            line = (
                -1 * slope,
                1,
                point_on_line[1] + (slope * point_on_line[0] * -1),
            )
            lines.add(line)
            key_sensors.add(((sensor1, radius1), (sensor2, radius2)))
    for eq1, eq2 in itertools.combinations(lines, 2):
        res = line_intersection(eq1, eq2)
        if res is not False:
            if not is_point_covered(res, sensors):
                ans2 = res[0] * 4_000_000 + res[1]
                break

    return no_beacons, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

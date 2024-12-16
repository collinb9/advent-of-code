import sys
from lib.datastructures import Array
from lib.utils import rotate_90, rotate_270
import collections


DIRECTIONS = [
    Array.up,
    Array.right,
    Array.down,
    Array.left,
]


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line) for line in fp.read().splitlines()]

    return data


def count_sides(array: Array, border, start_val):
    """
    The strategy is to find all cycles in the set of boundary points.
    Once each cycle is found, the number of sides is just the number of
    90 degree turns.
    """
    intersections = set()
    for _node in border:
        if all(
            neighbour in border
            for neighbour in array.find_adjacent_with_boundary(*_node)
        ):
            intersections.add(_node)
    # Never start at an intersection
    # Have to handle intersection points differently since they will
    # be part of two different cycles
    border = border - intersections
    sides = 0
    while border:
        start_node = border.pop()
        exit_dirs = {}
        cycle = []
        cycle.append((start_node, start_node))
        cycle_finished = False
        while not cycle_finished:
            valid_directions = DIRECTIONS
            current_node, previous_node = cycle[-1]
            if (
                current_node in intersections
            ):  # At an intesection, you should always turn "inward"
                for _dir in DIRECTIONS:
                    if (
                        array.loc(
                            previous_node[0] + _dir[0],
                            previous_node[1] + _dir[1],
                        )
                        == start_val
                    ):
                        valid_directions = [_dir]
                        break

            for _dir in valid_directions:
                (ii, jj) = (
                    current_node[0] + _dir[0],
                    current_node[1] + _dir[1],
                )
                if (ii, jj) == previous_node:
                    continue

                if ((ii, jj), (ii, jj)) in cycle:  # Cycle complete
                    if (
                        _dir != exit_dirs[(ii, jj)]
                        or _dir != exit_dirs[previous_node]
                    ):  # Check if the cycle ends on a corner
                        sides += 1

                    cycle_finished = True
                    cycle = []
                    break
                if (ii, jj) in border.union(intersections):
                    if (
                        current_node != start_node
                        and _dir != exit_dirs[previous_node]
                    ):
                        sides += 1
                    exit_dirs[current_node] = _dir
                    cycle.append(((ii, jj), current_node))
                    if (ii, jj) not in intersections:
                        border.remove((ii, jj))
                    break
            else:
                raise ValueError("No valid direction found")
    return sides


def fill(array, start, covered: set, val):
    stack = [start]
    covered.add(start)
    border = set()
    volume, perimeter = 1, 0
    while stack:
        loc = stack.pop()
        for _dir in DIRECTIONS:
            ii, jj = loc[0] + 2 * _dir[0], loc[1] + 2 * _dir[1]
            if array.loc(ii, jj) != val:
                first_border = (loc[0] + _dir[0], loc[1] + _dir[1])
                # Rotate 90 degrees
                second_border = (
                    first_border[0] + _dir[1] * -1,
                    first_border[1] + _dir[0],
                )
                # Rotate 270 degress is mult by i^3 = -i
                # (x + iy) * -i -> y - xi, (x, y) -> (y, -x)
                third_border = (
                    first_border[0] + _dir[1],
                    first_border[1] + _dir[0] * -1,
                )
                border.add(first_border)
                border.add(second_border)
                border.add(third_border)

                perimeter += 1
            elif (ii, jj) not in covered:
                volume += 1
                covered.add((ii, jj))
                stack.append((ii, jj))

    return volume, perimeter, border, covered


def main(fpath):
    data = read_data(fpath)
    array = Array(data)

    covered = set()

    ans1 = 0
    ans2 = 0

    # Add a gap between all entries to allow drawing the border
    new_data = {}
    for ii, jj in array.grid:
        new_data[(ii * 2, jj * 2)] = array.loc(ii, jj)

    array = array.from_dict(new_data)

    for ii, jj in array.grid:
        if ii % 2 == 0 and jj % 2 == 0:
            if (ii, jj) not in covered:
                val = array.loc(ii, jj)
                volume, perimeter, border, covered = fill(
                    array, (ii, jj), covered, val
                )
                ans1 += volume * perimeter
                sides = count_sides(array, border, val)
                ans2 += volume * sides

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

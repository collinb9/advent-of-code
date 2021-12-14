import sys
import itertools


def read_data(fpath):
    data = set()
    instructions = []
    with open(fpath, "r") as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            if not line.strip():
                break
            data.add(tuple(map(int, line.strip().split(","))))

        for line in lines[i:]:
            if line.strip():
                tmp = line.strip().split(" ")[-1].split("=")
                tmp[1] = int(tmp[1])
                instructions.append(tmp)
    return data, instructions


def main(fpath):
    data, instructions = read_data(fpath)
    for (axis, value) in instructions:
        new_data = set()
        index = int(axis == "y")
        for point in data:
            if point[index] > abs(value):
                diff = abs(value - point[index])
                new_point = (
                    point[0] - (2 * diff) * (1 - index),
                    point[1] - (2 * diff) * (index),
                )
                new_data.add(new_point)
            else:
                new_data.add(point)
        data = new_data
        yield new_data


if __name__ == "__main__":
    fpath = sys.argv[1]
    for i, val in enumerate(main(fpath)):
        if i == 0:
            print("Answer 1: ", len(val))

    # Display the answer to part 2 in a grid
    x, y = max([p[0] for p in val]) + 1, max([p[1] for p in val]) + 1
    grid = [[" "] * x for _ in range(y)]
    for i, j in itertools.product(range(x), range(y)):
        if (i, j) in val:
            grid[j][i] = "#"
    print("Answer 2: ")
    for i in grid:
        for j in i:
            print(j, end=" ")
        print()

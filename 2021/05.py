import sys
import itertools
import collections


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.split("->") for line in fp.readlines()]
        data = [coords.split(",") for line in data for coords in line]
        data = [[int(coord) for coord in line] for line in data]
    lines = []
    for i, point in enumerate(data):
        if not i % 2:
            temp_point = point
        else:
            lines.append([temp_point, point])

    return lines


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.x1 = p1[0]
        self.x2 = p2[0]
        self.y1 = p1[1]
        self.y2 = p2[1]
        self.max_y, self.min_y = max([self.y1, self.y2]), min(
            [self.y1, self.y2]
        )
        self.max_x, self.min_x = max([self.x1, self.x2]), min(
            [self.x1, self.x2]
        )

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"

    @property
    def all_coords(self):
        coords = []
        if self.x1 == self.x2:
            for y in range(self.min_y, self.max_y + 1):
                coords.append([self.x1, y])
        elif self.y1 == self.y2:
            for x in range(self.min_x, self.max_x + 1):
                coords.append([x, self.y1])
        else:  # diagonal
            if self.x1 < self.x2:
                x_range = range(self.x1, self.x2 + 1)
                if self.y1 <= self.y2:
                    y_range = range(self.y1, self.y2 + 1)
                else:
                    y_range = reversed(range(self.y2, self.y1 + 1))
            else:
                x_range = range(self.x2, self.x1 + 1)
                if self.y2 <= self.y1:
                    y_range = range(self.y2, self.y1 + 1)
                else:
                    y_range = reversed(range(self.y1, self.y2 + 1))
            for x, y in zip(x_range, y_range):
                coords.append([x, y])
        return coords


def main(fpath, no_diag=True):
    data = read_data(fpath)
    hits = collections.Counter()
    for line in data:
        line = Line(line[0], line[1])
        if no_diag:
            if line.x1 == line.x2 or line.y1 == line.y2:
                for coord in line.all_coords:
                    hits[str(coord)] += 1
        else:
            for coord in line.all_coords:
                hits[str(coord)] += 1

    count = 0
    for item, num in hits.items():
        if num >= 2:
            count += 1
    return count


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = main(fpath)
    print("Answer 1: ", answer_1)
    answer_2 = main(fpath, no_diag=False)
    print("Answer 2: ", answer_2)

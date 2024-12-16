import sys
import re
from lib.datastructures import Array
from collections import defaultdict
import itertools
import copy


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = list(map(int, list(fp.read().splitlines()[0])))

    return data


def part1(data):
    index = 0
    res = 0
    while data:
        _id, entry = data.pop(0)
        if _id is None:  # Need to fill the empty space
            while data:
                last_id, last_entry = data.pop(-1)
                if last_id is None:
                    pass
                else:
                    break
            if last_entry <= entry:
                res += sum(
                    ii * last_id for ii in range(index, index + last_entry)
                )
                index += last_entry
                entry = entry - last_entry
                if entry > 0:
                    data = [[_id, entry]] + data
            elif last_entry > entry:
                res += sum(ii * last_id for ii in range(index, index + entry))
                index += entry
                data.append([last_id, last_entry - entry])
                entry = 0

            if entry == 0:
                continue

        else:
            res += sum(ii * _id for ii in range(index, index + entry))
            index += entry
    return res


def part2(data):
    res = 0
    index = sum(entry for _, entry in data)
    while data:
        file_id, file_entry = data.pop()
        if file_id is None:  # Empty space
            index -= file_entry
            continue
        if file_entry == 0:  # Previouslsly empty, occupied by file(s)
            continue
        # Found a file
        for ii, (_id, entry) in enumerate(data):
            if _id is None:  # Found empty space
                if file_entry <= entry:  # Can fit file inside the space
                    data = (
                        data[:ii]
                        + [[file_id, file_entry]]
                        + [[_id, entry - file_entry]]
                        + data[ii + 1 :]
                    )
                    index -= file_entry
                    break
        else:  # File won't move
            res += sum(ii * file_id for ii in range(index - file_entry, index))
            index -= file_entry
    return res


def main(fpath):
    disk_map = read_data(fpath)

    ans1 = 0
    ans2 = 0

    data = []
    for i, entry in enumerate(disk_map):
        _id = None
        if i % 2 == 0:
            _id = int(i / 2)
        data.append([_id, entry])

    data2 = copy.deepcopy(data)
    ans1 = part1(data)
    ans2 = part2(data2)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

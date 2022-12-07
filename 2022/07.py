import sys
from pathlib import Path


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().split("\n")

    return data


def main(fpath):
    data = read_data(fpath)

    ### Parse input for directory hierarchy and file sizes
    ls = False
    _count = 0
    cwd = ""
    structure = {}
    sizes = {}
    for line in data:
        if ls and not line.startswith("$") and not line=="":
            if line.startswith("dir"):
                structure.setdefault(cwd, []).append(str(Path(cwd) / line.split(" ")[-1]))
            else:
                size = int(line.split(" ")[0])
                _count += size


        if ls and line.startswith("$"): # End of ls output
            if cwd not in sizes:
                sizes[cwd] = _count
            _count = 0

        if line.startswith("$ cd"):
            new_dir = line.split(" ")[-1]
            if new_dir == "..":
                cwd = str(Path(cwd).parents[0])
            else:
                cwd = str(Path(cwd) / new_dir)

        if line.startswith("$"):
            ls = False

        if line.startswith("$ ls"):
            ls = True
    #Handle last line
    sizes[cwd] = _count

    ### DFS to calculate the recursive size of each directory
    total_sizes = {}
    to_visit = ["/"]
    visited = set()
    while len(to_visit) > 0:
        current_dir = to_visit[-1]
        subdirs = structure.get(current_dir, [])
        if len(subdirs) == 0 or current_dir in visited:
            total_sizes[current_dir] = sizes[current_dir] + sum([total_sizes[_dir] for _dir in structure.get(current_dir, [])])
            to_visit.pop()
        else:
            for _dir in subdirs:
                to_visit.append(_dir)
        visited.add(current_dir)

    ### Part 1
    count = 0
    for value in total_sizes.values():
        if value <= 100000:
            count += value

    ### Part 2
    unused_space = 70000000 - total_sizes["/"]
    to_delete = 30000000 - unused_space
    size_to_delete = None
    for k, v in total_sizes.items():
        if v >= to_delete:
            if size_to_delete is None:
                size_to_delete = v
            elif v < size_to_delete:
                size_to_delete = v

    return count, size_to_delete


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

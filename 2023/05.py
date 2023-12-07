import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.utils import intervals_intersect


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    inner = []
    outer = []
    for dat in data:
        if dat:
            inner.append(dat)
        else:
            outer.append(inner)
            inner = []
    outer.append(inner)
    return outer


def map_seeds(seed_intervals, maps_list):
    for maps in maps_list:
        stack = list(seed_intervals)
        while len(stack) > 0:
            seed_interval = stack.pop()
            for line in maps[1:]:
                dest, source, _len = map(int, line.split())
                # Seed is mapped in this map
                if intervals_intersect(seed_interval, [(source, source + _len - 1)]):
                    seed_intervals.remove(seed_interval)
                    # Seeds which are not mapped in this line need to be checked against future lines in the same map
                    if seed_interval[0] < source:
                        stack.append((seed_interval[0], source - 1))
                    if seed_interval[1] >= source + _len:
                        stack.append((source + _len, seed_interval[1]))
                    if seed_interval[0] > source:
                        start = seed_interval[0]
                    else:
                        start = source
                    if seed_interval[1] < source + _len - 1:
                        end = seed_interval[1]
                    else:
                        end = source + _len - 1
                    # Seeds which are handled should not be checked against future lines in this map
                    seed_intervals.add((start + dest - source, end + dest - source))
                    break  # Move on to next map
            # Collect all seeds together before moving on to next map
            seed_intervals = seed_intervals | set(stack)
    return seed_intervals


def main(fpath):
    data = read_data(fpath)
    seeds = list(map(int, data[0][0].split(":")[-1].split()))
    # This is sort of stupid for part 1, but let's me use the same function for both parts
    ans1 = min(min(map_seeds(set((seed, seed) for seed in seeds), data[1:])))
    ans2 = min(
        min(
            map_seeds(
                set(
                    (seeds[i], seeds[i] + seeds[i + 1] - 1)
                    for i in range(0, len(seeds) - 1, 2)
                ),
                data[1:],
            )
        )
    )

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

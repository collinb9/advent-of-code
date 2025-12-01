import sys
from lib.datastructures import Array
import itertools

EMPTY = "."
FILLED = "#"


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line) for line in fp.read().splitlines()]

    keys, locks = [], []
    current = []
    for line in data:
        if not line:
            current = Array(data=current)
            if current.loc(0, 0) == EMPTY:
                keys.append(current)
            else:
                locks.append(current)
            current = []

        else:
            current.append(line)
    current = Array(data=current)
    if current.loc(0, 0) == EMPTY:
        keys.append(current)
    else:
        locks.append(current)
    return keys, locks


def main(fpath):
    keys, locks = read_data(fpath)
    # print(keys)
    # print()
    # print(locks)

    ans1 = 0
    ans2 = 0

    lock_columns = []
    for lock in locks:
        _lock = [-1 for _ in range(lock.x)]
        for ii, jj in lock.grid:
            if lock.loc(ii, jj) == FILLED:
                _lock[ii] += 1
        lock_columns.append(_lock)

    key_columns = []
    for key in keys:
        _key = [-1 for _ in range(key.x)]
        for ii, jj in key.grid:
            if key.loc(ii, jj) == FILLED:
                _key[ii] += 1
        key_columns.append(_key)

    # print(lock_columns)
    # print(key_columns)
    for _lock in lock_columns:
        for (
            _key
        ) in key_columns:  #  in itertools.product(lock_columns, key_columns):
            # print("Lock:", _lock, "Key:", _key)
            if all(aa + bb + 2 <= lock.y for aa, bb in zip(_lock, _key)):
                ans1 += 1

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys
import json
import itertools
import functools
import bisect


def read_data(fpath):
    with open(fpath, "r") as fp:
        _data = fp.read().split("\n\n")

    data = []
    for item in _data:
        if item:
            left, right = item.replace("\n", " ").strip().split(" ")
            data.append([json.loads(left), json.loads(right)])

    return data


def compare(left, right):
    for ll, rr in itertools.zip_longest(left, right):
        if ll is None:
            return -1
        elif rr is None:
            return 1
        if isinstance(ll, int) and isinstance(rr, int):
            if rr < ll:
                return 1
            if ll < rr:
                return -1
            else:
                continue
        elif isinstance(ll, list) and isinstance(rr, int):
            rr = [rr]
        elif isinstance(rr, list) and isinstance(ll, int):
            ll = [ll]
        res = compare(ll, rr)
        if res == 0:
            continue
        return res
    return 0


def main(fpath):
    data = read_data(fpath)

    # Part 1
    ans1 = 0
    for i, (left, right) in enumerate(data, 1):
        if compare(left, right) == -1:
            ans1 += i

    # Part 2
    data = [_item for item in data for _item in item]
    key_func = functools.cmp_to_key(compare)
    data.sort(key=key_func)
    key1 = (
        bisect.bisect_left(
            a=data,
            x=key_func([[2]]),
            key=functools.cmp_to_key(compare),
        )
        + 1
    )
    key2 = (
        bisect.bisect_left(
            a=data,
            x=key_func([[6]]),
            key=functools.cmp_to_key(compare),
        )
        + 2
    )

    return ans1, key1 * key2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

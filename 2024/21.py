import sys
from lib.metrics import manhattan
from lib.datastructures import BaseArray


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line for line in fp.read().splitlines()]

    return data


KEYPAD = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
    "EMPTY": (0, 3),
}

DIRECTIONPAD = {
    BaseArray.up: (1, 0),
    BaseArray.down: (1, 1),
    BaseArray.left: (0, 1),
    BaseArray.right: (2, 1),
    "A": (2, 0),
    "EMPTY": (0, 0),
}


def move(_next, current, avoid):
    _dir = (_next[0] - current[0], _next[1] - current[1])
    vert = _dir[1]
    horiz = _dir[0]
    # print("next:", _next, "current:", current, "dir:", _dir)
    if horiz < 0:
        horiz = (BaseArray.left, abs(horiz))
    elif horiz > 0:
        horiz = (BaseArray.right, abs(horiz))
    else:
        horiz = (None, 0)
    if vert > 0:
        vert = (BaseArray.down, abs(vert))
    elif vert < 0:
        vert = (BaseArray.up, abs(vert))
    else:
        vert = (None, 0)
    if current[1] == avoid[1]:
        return [vert, horiz]
    return [horiz, vert]


def shortest_sequence_number_pad(code, start="A"):
    start = KEYPAD[start]
    current = start
    seq = []
    for _char in code:
        _next = KEYPAD[_char]
        seq.append(move(_next, current, avoid=KEYPAD["EMPTY"]))
        current = _next
        seq.append(["A", 1])
    print(stringify(seq))
    # _seq = seq
    a_count = shortest_sequence_direction_pad(seq, depth=0, a_count=4)
    # print(_seq)

    return a_count


def stringify(seq):
    res = ""
    MAPPING = {
        BaseArray.up: "^",
        BaseArray.down: "v",
        BaseArray.left: "<",
        BaseArray.right: ">",
        (2, 0): "A",
        (2, 3): "A",
    }
    for pair in seq:
        if pair[0] == "A":
            res += "A" * pair[1]
            continue
        for _dir, count in pair:
            if _dir is not None:
                res += MAPPING[_dir] * count
        # res += "A"
    return res


def shortest_sequence_direction_pad(
    directions, depth=0, start="A", a_count=0, _diff=0
):
    seq = []
    _start = DIRECTIONPAD[start]
    # _start = (2, 0)
    current = _start
    _a_count = 0
    diff = a_count - len(directions)
    for pair in directions:
        # Follow directions
        stay = True
        if pair[0] == "A":  # When we hit an "A", we should already be there
            count = pair[1]
            _next = DIRECTIONPAD["A"]
            _a_count += count
            seq.append(move(_next, current, avoid=DIRECTIONPAD["EMPTY"]))
            seq.append(["A", count])
            current = _next
            continue
        #     res += "A" * pair[1]
        #     continue
        # (_dir1, _), (_dir2, _) = pair
        # dist1 = manhattan(current, DIRECTIONPAD[_dir1])
        # dist2 = manhattan(current, DIRECTIONPAD[_dir1])
        pair = sorted(
            pair,
            key=lambda x: manhattan(DIRECTIONPAD[x[0]], current)
            if x[0] is not None
            else 0,
        )
        for _dir, count in pair:  # (horiz, vert)
            # _dir = (-1, 0), count = 1
            if _dir is not None:
                stay = False
                _next = DIRECTIONPAD[_dir]
                # _next = (0, 1)
                # current = (2, 0)
                # print("Next:", _next, "Current:", current)
                _move = move(_next, current, avoid=DIRECTIONPAD["EMPTY"])
                # print("Move:", _move)
                seq.append(_move)
                # print("Seq", seq)
                current = _next
                _a_count += count
                seq.append(["A", count])
                # _next = DIRECTIONPAD["A"]
                # seq.append(move(_next, current, avoid=DIRECTIONPAD["EMPTY"]))
                # current = _next

        # if stay:
        #     print("Staying put")
        #     seq.append(move(_next, current, avoid=DIRECTIONPAD["EMPTY"]))
        # _a_count += 1
        # Press "A"
        # _next = DIRECTIONPAD["A"]
        # seq.append(move(_next, current, avoid=DIRECTIONPAD["EMPTY"]))
        # _a_count += 1
        # seq.append(["A", 1])
        # seq.append(["A", 1])
        # seq.append(["A", 1])

        current = _next
        # break

    print()
    # print(seq)
    print(stringify(seq))
    print(
        "A count:",
        _a_count,
        "Last A count:",
        a_count,
        "Diff:",
        diff,
        "Last Diff:",
        _diff,
    )
    if depth <= 0:
        return shortest_sequence_direction_pad(
            seq, depth + 1, start, _a_count + diff, _diff=diff
        )
    # return sum(_dir1[1] + _dir2[1] for _dir1, _dir2 in seq)
    # The number of times that A is pressed next time, is the length of this sequence
    # return _a_count + diff
    return len(stringify(seq))


def main(fpath):
    data = read_data(fpath)
    # print(data)

    ans1 = 0
    ans2 = 0

    for code in data:
        numeric = int(code[:-1])
        a_count = shortest_sequence_number_pad(code)  # * numeric
        print("A count:", a_count, "Numberic", numeric)  # 29
        # ans1 += sum(_dir1[1] + _dir2[1] for _dir1, _dir2 in seq) + a_count
        ans1 += a_count * numeric

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

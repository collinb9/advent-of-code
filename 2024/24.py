import sys
import collections
import itertools
from functools import partial


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line for line in fp.read().splitlines()]

    outer = []
    inner = []
    for line in data:
        if not line:
            outer.append(inner)
            inner = []
            continue
        inner.append(line)
    outer.append(inner)
    return outer


# def and(xx, yy):
#     return xx and yy


def get_bin_number(values, starts_with):
    _values = {
        key: value
        for key, value in values.items()
        if key.startswith(starts_with)
    }
    res = "".join(
        [
            str(value)
            for _, value in sorted(
                _values.items(),
                reverse=True,
            )
        ]
    )
    return res


def main(fpath):
    initial_values, _connections = read_data(fpath)
    values = {
        key: int(value)
        for item in initial_values
        for key, value in [item.split(": ")]
    }

    _x = get_bin_number(values, "x")
    _y = get_bin_number(values, "y")
    print("X:", _x)
    print("Y:", _y)
    expected_result = int(_x, 2) & int(_y, 2)
    print("Expected Result: ", expected_result)
    expected_result_string = str(bin(expected_result)[2:])
    print("Binary representation: ", expected_result_string)
    expected_values = {}
    for ii, bit in enumerate(expected_result_string[::-1]):
        expected_values[f"z{ii:02}"] = bit
    print(expected_values)

    connections = collections.defaultdict(
        partial(collections.defaultdict, list)
    )
    for connection in _connections:
        in1, _gate, in2, _, out = connection.split()
        connections[in2][in1].append((_gate, out))
        connections[in1][in2].append((_gate, out))

    ans1 = 0
    ans2 = 0

    # stack = list(itertools.combinations(values.keys(), 2))
    # DfS
    queue = collections.deque(values.keys())

    # seen = set()
    while len(queue) > 0:
        # for connection in connections:
        # for connection in connections:
        in1 = queue.popleft()
        # in1, _gate, in2, _, out = connection.split()
        value_1 = values.get(in1)
        if value_1 is None:
            # No value set for wire, try again later
            queue.append(in1)
            continue
        for in2, gates in connections[in1].items():
            for _gate, out in gates:
                value_2 = values.get(in2)
                if value_2 is None:
                    # queue.append()
                    continue
                if out in values:
                    continue
                if _gate == "AND":
                    values[out] = int(value_1 and value_2)
                elif _gate == "OR":
                    values[out] = int(value_1 or value_2)
                elif _gate == "XOR":
                    values[out] = value_1 ^ value_2
                queue.append(out)

    res = {key: value for key, value in values.items() if key.startswith("z")}
    ans1 = int(
        "".join(
            [str(value) for _, value in sorted(res.items(), reverse=True)]
        ),
        2,
    )

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

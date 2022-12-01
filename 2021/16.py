import sys
import functools
import collections
import operator


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.strip() for line in fp.readlines()]
    res = []
    for num in data:
        num_bin = ""
        for char in num:
            char_bin = bin(int(char, 16))[2:]
            size = len(char_bin)
            char_bin = "0" * (4 - size) + char_bin
            num_bin = num_bin + char_bin
        res.append(num_bin)

    return res


OPERATIONS = [
    operator.add,
    operator.mul,
    min,
    max,
    lambda a, b: a,
    operator.gt,
    operator.lt,
    operator.eq,
]


def bin_pop(num, n):
    res = []
    for _ in range(n):
        res.append(num.popleft())
    return "".join(res)


def bin_to_num(data):
    return int(data, 2)


def solve(num):
    global version_sum
    if not num or bin_to_num("".join(num)) == 0:
        return
    version = bin_pop(num, 3)
    type_id = bin_pop(num, 3)
    version_sum += bin_to_num(version)
    type_id = bin_to_num(type_id)
    operation = OPERATIONS[type_id]

    def inner():
        if type_id == 4:
            indicator = "1"
            literal = ""
            while indicator == "1":
                indicator = bin_pop(num, 1)
                next_part = bin_pop(num, 4)
                literal = literal + next_part
            literal = bin_to_num(literal)
            yield literal
        else:
            length_type_id = bin_pop(num, 1)
            if length_type_id == "0":
                length_sub_packets = bin_pop(num, 15)
                length_sub_packets = bin_to_num(length_sub_packets)
                remainder = len(num) - length_sub_packets
                while len(num) > remainder:
                    yield solve(num)
            else:
                num_subpackets = bin_pop(num, 11)
                num_subpackets = bin_to_num(num_subpackets)
                for _ in range(num_subpackets):
                    yield solve(num)

    return functools.reduce(operation, inner())


def main(fpath):
    data = read_data(fpath)

    global version_sum
    # Looping for test cases, actual input requires no loop
    for num in data:
        version_sum = 0
        num = collections.deque(list(num))
        res = solve(num)
    return version_sum, res


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)

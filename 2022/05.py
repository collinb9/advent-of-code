import sys
import copy


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]
    outer = []
    inner = []
    for dat in data:
        if dat:
            inner.append((dat))
        else:
            outer.append(inner)
            inner = []
    outer.append(inner)

    _stacks = outer[0]
    _stacks.pop()  # Remove indexes
    _stacks = [line[1::4] for line in _stacks]

    stacks = [[] for stack in _stacks[0]]
    for _stack in _stacks[
        ::-1
    ]:  # Reverse lists so top crate is last item in list
        for item, stack in zip(_stack, stacks):
            if item != " ":
                stack.append(item)

    _instructions = outer[1]
    instructions = [
        list(map(int, instruction.split(" ")[1::2]))
        for instruction in _instructions
    ]

    return stacks, instructions


def get_top_crates(stacks):
    return "".join([stack[-1] for stack in stacks])


def main(fpath):
    stacks, instructions = read_data(fpath)
    stacks_1 = copy.deepcopy(stacks)
    stacks_2 = copy.deepcopy(stacks)
    for instruction in instructions:
        amount, _from, _to = instruction
        # Part 1
        for _ in range(amount):
            stacks_1[_to - 1].append(stacks_1[_from - 1].pop())
        # Part 2
        stacks_2[_to - 1].extend(stacks_2[_from - 1][-1 * amount :])
        stacks_2[_from - 1] = stacks_2[_from - 1][: -1 * amount]
    return get_top_crates(stacks_1), get_top_crates(stacks_2)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

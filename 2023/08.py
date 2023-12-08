import sys
import itertools
import math


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    _instructions = data[0].replace("R", "1").replace("L", "0")
    network = dict()
    for line in data[2:]:
        parent, children = line.split("=")
        left, right = children.replace("(", "").replace(")", "").split(",")
        parent, left, right = parent.strip(), left.strip(), right.strip()
        network[parent] = (left, right)

    # Part 1
    node = "AAA"
    instructions = itertools.cycle(_instructions)
    for ans1, direction in enumerate(instructions):
        if node == "ZZZ":
            break
        node = network[node][int(direction)]

    # Part 2
    start_nodes = []
    for node in network:
        if node.endswith("A"):
            start_nodes.append(node)

    # There must be cycles in the data.
    # For each start point, check how long the cycles are, and where to find each
    # term ending in "Z", and use that to calculate the answer.
    # What we need to calculate the answer:
    #   - When the cycle starts
    #   - How long a cycle
    #   - Where all items ending in Z were found in the cycle

    # Properties of the input:
    # - There is only 1 z value found from each starting node.
    # - Each Z value is at the ith step, where the length of the cycle it is contained in is of lenght i.
    # Knowing these things simplifies things greatly
    z_values = []
    for start_node in start_nodes:
        node = start_node
        seen = dict()
        instructions = itertools.cycle(_instructions)
        for i, direction in enumerate(instructions):
            instruction_index = i % len(_instructions)
            if (node, instruction_index) in seen:
                break
            if node.endswith("Z"):
                z_value = i
            seen[(node, instruction_index)] = i
            node = network[node][int(direction)]
        z_values.append(z_value)
    ans2 = math.lcm(*z_values)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

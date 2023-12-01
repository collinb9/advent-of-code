import sys
import json
import math
import copy
import functools
import itertools
import collections


class Node:
    """
    A node in a binary tree

    State is kept about the node
        * left node
        * right node
        * parent node
        * value
        * depth in the tree
        * A unique identifier
    """

    def __init__(self, _id, left=None, right=None, parent=None, value=None, depth=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.value = value
        self.depth = depth
        self.id = _id

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, left={self.left}, right={self.right}, parent={self.parent}, depth={self.depth}, value={self.value})>"


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [json.loads(line.strip()) for line in fp.readlines()]
    return data


def parse_data_to_binary_tree(data):
    nodes = {}
    node_number = 0

    def inner(data, depth=0, parent=None):
        nonlocal node_number, nodes
        current_node_number = node_number
        node = Node(current_node_number, parent=parent)
        node.depth = depth
        nodes[current_node_number] = node
        if isinstance(data, int):
            node.value = data
            return node

        node_number += 1
        node.left = node_number
        inner(data[0], depth=depth + 1, parent=current_node_number)
        node_number += 1
        node.right = node_number
        inner(data[1], depth=depth + 1, parent=current_node_number)
        return node

    inner(data, 0)
    return nodes


def parse_binary_tree_to_lists(binary_tree):
    root_node = binary_tree[0]
    # Traverse binary tree depth first
    queue = collections.deque()
    result = []
    queue.append((root_node, result))
    while len(queue) > 0:
        node, child_level = queue.popleft()
        for child_id in [node.left, node.right]:
            child_node = binary_tree[child_id]
            if child_node.value is None:
                next_child_level = []
                child_level.append(next_child_level)
                queue.append((child_node, next_child_level))
            else:
                child_level.append(child_node.value)
    return result


def depth_first_search_for_explode_condition(binary_tree, depth=4):
    node = binary_tree[0]
    stack = collections.deque()
    stack.append(node)
    while len(stack) > 0:
        node = stack.pop()
        if (
            node.depth >= depth
            and binary_tree[node.left].value is not None
            and binary_tree[node.right].value is not None
        ):
            return node
        for child_id in [node.right, node.left]:
            child_node = binary_tree[child_id]
            if child_node.value is None:
                stack.append(child_node)

    return None


def depth_first_search_for_split_condition(binary_tree, value=10):
    node = binary_tree[0]
    stack = collections.deque()
    stack.append(node)
    while len(stack) > 0:
        node = stack.pop()
        if node.value is not None and node.value >= value:
            return node
        for child_id in [node.right, node.left]:
            if child_id is not None:
                child_node = binary_tree[child_id]
                stack.append(child_node)

    return None


def recurse_left(bin_tree, node: Node):
    if node.value is not None:
        return node
    return recurse_left(bin_tree, bin_tree[node.left])


def recurse_right(bin_tree, node: Node):
    if node.value is not None:
        return node
    return recurse_right(bin_tree, bin_tree[node.right])


def find_next_leaf_node_left(bin_tree, node: Node):
    parent_id = node.parent
    if parent_id is None:  # We've hit the root node
        return None
    parent = bin_tree[parent_id]
    if parent.left != node.id:
        if bin_tree[parent.left].value is not None:  # logic for going up the tree
            return bin_tree[parent.left]
        else:  # Logic for going down the tree
            return recurse_right(bin_tree, bin_tree[parent.left])
    return find_next_leaf_node_left(bin_tree, parent)


def find_next_leaf_node_right(bin_tree, node: Node):
    parent_id = node.parent
    if parent_id is None:  # We've hit the root node
        return None
    parent = bin_tree[parent_id]
    if parent.right != node.id:
        if bin_tree[parent.right].value is not None:  # logic for going up the tree
            return bin_tree[parent.right]
        else:  # Logic for going down the tree
            return recurse_left(bin_tree, bin_tree[parent.right])
    return find_next_leaf_node_right(bin_tree, parent)


def add(number1, number2):
    """
    Add together the binary tree representations of snailnumbers

    Convert binary tree to a list of lists, add and then reconvert.
    There is probably a faster way to do this, but this is the easiest
    """
    number1 = parse_binary_tree_to_lists(number1)
    number2 = parse_binary_tree_to_lists(number2)
    return parse_data_to_binary_tree([number1, number2])


def add_first_2_pairs(snailfish_numbers):
    return [add(snailfish_numbers.pop(0), snailfish_numbers.pop(0))] + snailfish_numbers


def explode(bin_tree, node):
    next_node_left = find_next_leaf_node_left(bin_tree, node=node)
    if next_node_left is not None:
        next_node_left.value += bin_tree[node.left].value
    next_node_right = find_next_leaf_node_right(bin_tree, node=node)
    if next_node_right is not None:
        next_node_right.value += bin_tree[node.right].value
    # Delete exploded nodes
    del bin_tree[node.left]
    del bin_tree[node.right]
    node.left = None
    node.right = None
    node.value = 0
    return node


def split(binary_tree, node):
    max_id = max(binary_tree)

    binary_tree[max_id + 1] = Node(
        max_id + 1,
        parent=node.id,
        value=math.floor(node.value / 2),
        depth=node.depth + 1,
    )
    node.left = max_id + 1

    binary_tree[max_id + 2] = Node(
        max_id + 2,
        parent=node.id,
        value=math.ceil(node.value / 2),
        depth=node.depth + 1,
    )
    node.right = max_id + 2

    node.value = None


def reduce(snailfish_numbers):
    """
    Reduce the number

    Check if any node is explodeable
        - If there is, explode it and start again
        - else, check if any number is splitable
            - if it is, split it and start again
            - else, end
    """
    explodeable_node = depth_first_search_for_explode_condition(
        snailfish_numbers[0], depth=4
    )
    binary_tree = snailfish_numbers[0]
    if explodeable_node is not None:
        explode(binary_tree, explodeable_node)
        return reduce(snailfish_numbers)
    else:
        splitable_node = depth_first_search_for_split_condition(
            snailfish_numbers[0], value=10
        )
        if splitable_node is not None:
            split(binary_tree, splitable_node)
            return reduce(snailfish_numbers)

    return snailfish_numbers


def magnitude(bin_tree, node):
    if node.value is not None:
        return node.value

    return (
        magnitude(bin_tree, bin_tree[node.left]) * 3
        + magnitude(bin_tree, bin_tree[node.right]) * 2
    )


def main(fpath):
    data = read_data(fpath)

    ### Part 1
    # Parse data into an array of binary trees
    snailfish_numbers = []
    for number in data:
        binary_tree = parse_data_to_binary_tree(number)
        snailfish_numbers.append(binary_tree)

    while len(snailfish_numbers) > 1:
        snailfish_numbers = add_first_2_pairs(snailfish_numbers)
        snailfish_numbers = reduce(snailfish_numbers)
    final_binary_tree = snailfish_numbers[0]

    ### Part 2
    # Parse data into an array of binary trees
    snailfish_numbers = []
    for number in data:
        binary_tree = parse_data_to_binary_tree(number)
        snailfish_numbers.append(binary_tree)

    # For each pariwise comnination of snailfish numbers, compute the magnitude of the sum and then find the max magnitude
    magnitudes = []
    for number1, number2 in itertools.permutations(snailfish_numbers, 2):
        sum = add(number1, number2)
        reduced_sum = reduce([sum])[0]
        mag = magnitude(reduced_sum, reduced_sum[0])
        magnitudes.append(mag)

    return magnitude(final_binary_tree, final_binary_tree[0]), max(magnitudes)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)

import sys
import json
import math
import functools
import itertools
import collections

class Node:

    def __init__(self, _id, left = None, right = None, parent = None, value = None, depth = None):
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

    return data

def parse_data_to_binary_tree(data):
    nodes = {}
    node_number = 0

    def inner(data, depth = 0, parent = None):
        nonlocal node_number, nodes
        current_node_number = node_number
        node = Node(current_node_number, parent = parent)
        node.depth = depth
        nodes[current_node_number] = node
        if isinstance(data, int):
            node.value = data
            return node

        node_number += 1
        node.left = node_number
        inner(data[0], depth = depth +1, parent = current_node_number)
        node_number += 1
        node.right = node_number
        inner(data[1], depth = depth +1, parent = current_node_number )
        return node

    inner(data, 0)
    return nodes, node_number

def recurse_left(bin_tree, node: Node):
    if node.value is not None:
        return node
    return recurse_left(bin_tree, bin_tree[ node.left ])

def recurse_right(bin_tree, node: Node):
    if node.value is not None:
        return node
    return recurse_right(bin_tree, bin_tree[node.right])


def find_next_leaf_node_left(bin_tree, node: Node):
    # print("FINDING NEXT LEAF NODE LEFT FOR: ", node)
    parent_id = node.parent
    if parent_id is None: # We've hit the root node
        return None
    parent = bin_tree[parent_id]
    if parent.left != node.id:
        if bin_tree[parent.left].value is not None: # logic for going up the tree
            return bin_tree[parent.left]
        else: # Logic for going down the tree
            return recurse_right(bin_tree, bin_tree[parent.left])
    return find_next_leaf_node_left(bin_tree, parent)

def find_next_leaf_node_right(bin_tree, node: Node):
    # print("FINDING NEXT LEAF NODE RIGHT FOR: ", node)
    parent_id = node.parent
    if parent_id is None: # We've hit the root node
        return None
    parent = bin_tree[parent_id]
    if parent.right != node.id:
        if bin_tree[parent.right].value is not None: # logic for going up the tree
            return bin_tree[parent.right]
        else: # Logic for going down the tree
            return recurse_left(bin_tree, bin_tree[parent.right])
    return find_next_leaf_node_right(bin_tree, parent)

# def find_next_leaf_node_right(bin_tree, node: Node):
#     return Node(-1)

def reduce(data):
    bin_tree = parse_data_to_binary_tree(data)
    return bin_tree

def explode(node: Node):
    print("exploding ", node)

def split(node: Node):
    print("splitting ", node)

def bin_tree_to_list(bin_tree, node: Node):
    if node.value is not None:
        return node.value
    return [bin_tree_to_list(bin_tree, bin_tree[node.left]), bin_tree_to_list(bin_tree, bin_tree[node.right])]

def magnitude(bin_tree, node):
    if node.value is not None:
        return node.value

    return magnitude(bin_tree, bin_tree[node.left]) * 3 + magnitude(bin_tree, bin_tree[node.right]) * 2

def main(fpath):
    data = read_data(fpath)
    # print(data)
    # current = data[0]
    # print(bin_tree)
    current = []
    for item in data:
        print()
        print(item)
        # current = [current, item]
        if current:
            current = [current, item]
        else:
            current = item
        print(current)
        bin_tree, node_number = parse_data_to_binary_tree(current)
        print(bin_tree)
        stack = collections.deque()
        root_node = bin_tree[0]
        stack.append(root_node)
        split_stack = collections.deque()
        phase_1 = True
        while len(stack) > 0 or len(split_stack) > 0:
            if len(stack) > 0:
                node = stack.pop()
                _split = False
            else:
                phase_1 = False
                node = split_stack.pop()
                _split = True
            # print(node, _split)
            # print(node)
            # print(bin_tree_to_list(bin_tree, bin_tree[0]))
            if node.id not in bin_tree:
                continue
            if node.value is None:
                for next_node in [node.right, node.left]:
                    stack.append(bin_tree[next_node])
                continue
            if node.depth > 4: # explode
                parent = bin_tree[node.parent]
                # print("PARENT: ", parent)
                if bin_tree[parent.right].value is None or bin_tree[parent.left].value is None:
                    continue
                explode(parent)
                left, right = parent.left, parent.right
                left_node, right_node = bin_tree[left], bin_tree[right]
                print("EXPLODING ", left_node, " AND ", right_node)
                parent.left = None
                parent.right = None
                parent.value = 0
                del bin_tree[left]
                del bin_tree[right]
                stack.pop()
                next_node_left = find_next_leaf_node_left(bin_tree, parent)
                print("NEXT NODE LEFT: ", next_node_left)
                next_node_right = find_next_leaf_node_right(bin_tree, parent)
                print("NEXT NODE RIGHT: ", next_node_right)
                if next_node_left is not None:
                    # print("INCREMENTING VALUE OF LEFT NODE BY ", left_node.value)
                    next_node_left.value += left_node.value
                if next_node_right is not None:
                    # print("INCREMENTING VALUE OF RIGHT NODE BY ", right_node.value)
                    next_node_right.value += right_node.value
                stack.append(parent)
                if next_node_left is not None and next_node_left.id in bin_tree and phase_1:
                    split_stack.appendleft(next_node_left)
                if next_node_right is not None and next_node_right.id in bin_tree and phase_1:
                    split_stack.appendleft(next_node_right)
                if next_node_right is not None and next_node_right.id in bin_tree and not phase_1:
                    split_stack.append(next_node_right)
                if next_node_left is not None and next_node_left.id in bin_tree and not phase_1:
                    split_stack.append(next_node_left)
            elif _split and node.value is not None and node.value >= 10:
                split(node)
                node_number += 1
                node.left = node_number
                bin_tree[node_number] = Node(node_number, depth=node.depth + 1, parent = node.id, value = math.floor(node.value/2))
                node_number += 1
                node.right = node_number
                bin_tree[node_number] = Node(node_number, depth=node.depth + 1, parent = node.id, value = math.ceil(node.value/2))
                node.value = None
                stack.append(bin_tree[node.right])
                stack.append(bin_tree[node.left])
                split_stack.append(bin_tree[node.right])
                split_stack.append(bin_tree[node.left])
            print(bin_tree_to_list(bin_tree, bin_tree[0]))
        current = bin_tree_to_list(bin_tree, bin_tree[0])
        bin_tree.clear
    #     reduce(current)
    # print(current)
    print(bin_tree_to_list(bin_tree, bin_tree[0]))
    return magnitude(bin_tree, bin_tree[0])


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1= main(fpath)
    print("Answer 1: ", answer_1)
    # print("Answer 2: ", answer_2)

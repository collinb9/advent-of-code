import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lib.utils as utils
import re
import collections
import operator
import functools
import copy


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

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


def split_interval(interval, value, op, _min=1, _max=4000):
    if op == "<":
        top_left = min(interval[1], value - 1)
        bottom_right = max(value, interval[0])
    else:
        top_left = min(interval[1], value)
        bottom_right = max(value + 1, interval[0])

    if (value == interval[0] and op == ">") or value > interval[0]:
        left = (max(interval[0], _min), top_left)
    else:
        left = None
    if (value == interval[1] and op == "<") or value < interval[1]:
        right = (bottom_right, min(interval[1], _max))
    else:
        right = None
    return left, right

def find_workflow_containing_key(workflows, search_key):
    found = {}
    for key, workflow in workflows.items():
        *steps, end = workflow
        for step in steps:
            test, current = step
            if current == search_key:
                found.update({key: workflow})
                break
        else:
            if end[0] == search_key:
                found.update({key: workflow})
    return found

def main(fpath):
    _workflows, _ratings = read_data(fpath)

    workflows = dict()
    pattern = r"(.*){(.*)}"
    for _workflow in _workflows:
        res = re.search(pattern, _workflow)
        name, workflow = res.group(1), res.group(2)
        workflows[name] = [item.split(":") for item in workflow.split(",")]

    # [[x, m, a, s]]
    ratings = []
    for rating in _ratings:
        ratings.append(utils.ints(rating))

    ## Part 1
    ans1 = 0
    start = "in"
    for rating in ratings:
        x, m, a, s = rating
        current = start
        while True:
            if current == "R":
                break
            if current == "A":
                ans1 += sum(rating)
                break
            workflow = workflows[current]
            *steps, end = workflow
            for step in steps:
                test, current = step
                if eval(test):
                    break
            else:
                current = end[0]

    ## Part 2

    # DFS
    ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    accepted = []
    queue = collections.deque()
    queue.append((start, ranges, start))
    while len(queue) > 0:
        current, _ranges, prev = queue.popleft()
        if current == "R":
            continue
        if current == "A":
            accepted.append((prev, _ranges))
            continue
        prev = current
        workflow = workflows[current]
        *steps, end = workflow
        for step in steps:
            test, current = step
            test = test.split(">")
            if len(test) == 1:  # <
                op = "<"
                var, value = test[0].split("<")
                value = int(value)
            else:  # >
                op = ">"
                var, value = test
                value = int(value)
            left, right = split_interval(_ranges[var], value, op)
            if op == ">":
                fail = left
                success = right
            else:
                fail = right
                success = left

            success_ranges = copy.deepcopy(_ranges)
            if success is not None:
                success_ranges[var] = success
                queue.append((current, success_ranges, prev))
            if fail is not None:
                _ranges.update({var: fail})
            else:
                break

        else:
            current = end[0]
            queue.append((current, _ranges, prev))

    ans2 = 0
    for item in accepted:
        ans2 += functools.reduce(
            operator.mul, [val[1] - val[0] + 1 for val in item[1].values()]
        )

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys
import re
import math
from collections import defaultdict


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]
    outer = []
    inner = []
    for dat in data:
        if dat:
            inner.append(dat)
        else:
            outer.append(inner)
            inner = []
    outer.append(inner)

    first, second = outer
    orders = defaultdict(set)
    page_lists = []
    for item in first:
        key, value = item.split("|")
        orders[key].add(value)

    for item in second:
        page_lists.append(item.split(","))

    return orders, page_lists


def reorder(page_list, orders):
    for i, page in enumerate(page_list):
        for j, _page in enumerate(page_list[i + 1 :]):
            if _page not in orders[page]:  # rule broken
                page_list = (
                    page_list[:i]
                    + [_page, page]
                    + page_list[i + 1 : j + i + 1]
                    + page_list[j + i + 1 + 1 :]
                )
                return page_list, False
    return page_list, True


def main(fpath):
    orders, page_lists = read_data(fpath)
    ans1 = 0
    ans2 = 0

    for page_list in page_lists:
        for i, page in enumerate(page_list):
            for _page in page_list[i + 1 :]:
                if _page not in orders[page]:  # rule broken
                    break
            else:  # rule not broken
                continue
            break  # Rule broken
        else:  # Rule not broken
            ans1 += int(page_list[math.floor(len(page_list) / 2)])
            continue

        # Rule broken, need to reorder
        while True:
            page_list, result = reorder(page_list, orders)
            if result:
                ans2 += int(page_list[math.floor(len(page_list) / 2)])
                break

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

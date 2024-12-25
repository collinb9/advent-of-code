import sys
import collections
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.split("-") for line in fp.read().splitlines()]

    res = collections.defaultdict(set)
    for aa, bb in data:
        res[aa].add(bb)
        res[bb].add(aa)
    return res


def find_maximal_cliques(data):
    # Bron-Kerbosch
    clique = []

    def inner(r, p, x):
        nonlocal clique
        nonlocal data
        if not p and not x:
            if len(r) > len(clique):
                clique = r
        while p:
            node = p.pop()
            neighbours = data[node]
            node_set = set([node])
            inner(
                r.union(node_set),
                p.intersection(neighbours),
                x.intersection(neighbours),
            )
            x = x.union(node_set)
            p = p - node_set

    inner(set(), set(data.keys()), set())
    return clique


def main(fpath):
    data = read_data(fpath)

    ### Part 1
    ans1 = 0
    seen = set()
    for node, connections in data.items():
        if node in seen:
            continue
        if node.startswith("t"):
            for first, second in itertools.combinations(connections, 2):
                if second in data[first]:
                    if second.startswith("t"):
                        ans1 -= 1 / 2
                    if first.startswith("t"):
                        ans1 -= 1 / 2
                    ans1 += 1

    ### Part 2
    ans2 = ",".join(sorted(find_maximal_cliques(data)))

    return int(ans1), ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

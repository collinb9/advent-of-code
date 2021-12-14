import sys
import collections


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.strip().split("-") for line in fp.readlines()]
    return data


def next_nodes_problem_1(current_path, node):
    for next_node in graph[node]:
        if next_node.isupper() or next_node not in current_path:
            yield next_node


def next_nodes_problem_2(current_path, node):
    counter = collections.Counter([n for n in current_path if n.islower()])
    for next_node in graph[node]:
        if (
            next_node.isupper()
            or counter.most_common(1)[0][1] < 2
            or next_node not in current_path
        ):
            yield next_node


def main(next_node_strategy):
    """
    DFS. Not very fast, but it works ...
    """

    stack = collections.deque()
    paths = []
    stack.append(start)

    def inner(node, current_path):
        current_path.append(node)
        if node != end:
            for next_node in next_node_strategy(current_path[:], node):
                yield from inner(next_node, current_path[:])
        else:
            yield current_path

    paths = list(inner(start, []))
    return len(paths)


if __name__ == "__main__":
    fpath = sys.argv[1]

    data = read_data(fpath)
    graph = {}
    start = "start"
    end = "end"

    # parse data into a graph structure
    for edge in data:
        if start in edge:
            graph.setdefault(start, []).append(
                edge[(edge.index(start) + 1) % 2]
            )
        elif end in edge:
            graph.setdefault(edge[(edge.index(end) + 1) % 2], []).append(end)
        else:
            graph.setdefault(edge[0], []).append(edge[1])
            graph.setdefault(edge[1], []).append(edge[0])

    answer_1 = main(next_nodes_problem_1)
    print("Answer 1: ", answer_1)
    answer_2 = main(next_nodes_problem_2)
    print("Answer 2: ", answer_2)


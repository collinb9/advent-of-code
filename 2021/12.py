import sys
import collections

START = "start"
END = "end"

def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.strip().split("-") for line in fp.readlines()]
    graph = {}

    # parse data into a graph structure
    for edge in data:
        if START in edge:
            graph.setdefault(START, []).append(
                edge[(edge.index(START) + 1) % 2]
            )
        elif END in edge:
            graph.setdefault(edge[(edge.index(END) + 1) % 2], []).append(END)
        else:
            graph.setdefault(edge[0], []).append(edge[1])
            graph.setdefault(edge[1], []).append(edge[0])
    return graph


def next_nodes_problem_1(current_path, node, graph):
    for next_node in graph[node]:
        if next_node.isupper() or next_node not in current_path:
            yield next_node


def next_nodes_problem_2(current_path, node, graph):
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
    graph = read_data(fpath)

    def inner(node, current_path):
        current_path.append(node)
        if node != END:
            for next_node in next_node_strategy(current_path[:], node, graph):
                yield from inner(next_node, current_path[:])
        else:
            yield current_path

    paths = list(inner(START, []))
    return len(paths)


if __name__ == "__main__":
    fpath = sys.argv[1]


    answer_1 = main(next_nodes_problem_1)
    print("Answer 1: ", answer_1)
    answer_2 = main(next_nodes_problem_2)
    print("Answer 2: ", answer_2)


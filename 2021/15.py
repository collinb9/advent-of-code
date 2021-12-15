import sys
import itertools
import functools
import queue


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, list(line.strip()))) for line in fp.readlines()]
    return data

def adjacent(i, j, x, y):
    loc = [
        (i, min(j + 1, y - 1)),
        (i, max(0, j - 1)),
        (max(0, i - 1), j),
        (min(i + 1, x - 1), j),
    ]
    return [ll for ll in loc if ll != (i, j)]

def search(data):
    """
    Dijkstra
    """
    xx, yy = len(data[0]), len(data)
    sentinel = sum(itertools.chain.from_iterable(data))
    distances = [[sentinel for _ in range(xx)] for _ in range(yy)]
    distances[0][0] = 0
    priority_queue = queue.PriorityQueue()
    priority_queue.put((0, (0, 0)))
    seen = set()
    while not priority_queue.empty():
        current_distance, current = priority_queue.get()
        if current == (xx-1, yy-1):
            break
        for (ii, jj) in adjacent(current[0], current[1], xx, yy):
            if (ii, jj) not in seen:
                d = current_distance + data[jj][ii]
                if d < distances[jj][ii]:
                    distances[jj][ii] = d
                    priority_queue.put((distances[jj][ii], (ii, jj)))
        seen.add(current)
    return distances[yy-1][xx-1]

def new_block(data, n):
    xx, yy = len(data[0]), len(data)
    block = []
    for row in data:
        new_row = [((i - 1 + n) % 9) + 1 for i in row]
        block.append(new_row)
    return block

def append_columns(column_1, column_2):
    new_column  = []
    for row_1, row_2 in zip(column_1, column_2):
        new_column.append(row_1 + row_2)
    return new_column

def main(fpath):
    data = read_data(fpath)
    answer_1 = search(data)

    # Create extended grid
    columns = []
    for jj in range(5):
        blocks = []
        for ii in range(5):
            blocks.append(new_block(data, ii + jj))
        columns.append(blocks)
    for i, column in enumerate( columns ):
        columns[i] = list(itertools.chain.from_iterable(column))
    data = functools.reduce(append_columns, columns)

    answer_2 = search(data)

    return answer_1, answer_2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)


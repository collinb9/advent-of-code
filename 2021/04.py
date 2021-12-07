import sys
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split(",") for line in fp.readlines()]
    numbers = [int(n) for n in data[0]]
    board_data = []
    temp_board = []
    for dat in data[2:]:
        if dat[0]:
            dat = [int(num) for num in dat[0].split()]
            temp_board.append(dat)
        else:
            board_data.append(temp_board)
            temp_board = []
    board_data.append(temp_board)
    return numbers, board_data


class Board:
    def __init__(self, data):
        self.rows = [set(row) for row in data]
        self.columns = [
            set([row[i] for row in data]) for i in range(len(data[0]))
        ]

    @property
    def has_full_row(self):
        for row in self.rows:
            if not row:
                return True
        return False

    @property
    def has_full_column(self):
        for column in self.columns:
            if not column:
                return True
        return False

    @property
    def wins(self):
        return self.has_full_row or self.has_full_column

    @property
    def score(self):
        total = list(itertools.chain.from_iterable(self.rows))
        return sum(total)

    def read_number(self, number):
        for row in self.rows:
            if number in row:
                row.remove(number)
        for column in self.columns:
            if number in column:
                column.remove(number)


def main(fpath):
    numbers, board_data = read_data(fpath)
    boards = []
    for data in board_data:
        board = Board(data)
        boards.append(board)
    for num in numbers:
        for board in boards:
            if not board.wins:
                board.read_number(num)
                if board.wins:
                    yield board.score * num

    return 0


if __name__ == "__main__":
    fpath = sys.argv[1]
    for i, res in enumerate(main(fpath)):
        if i == 0:
            print("Answer 1: ", res)
    print("Answer 2: ", res)

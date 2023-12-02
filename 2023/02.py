import sys
from functools import reduce
import operator


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def parse_game(game):
    game_id, _sets = game.split(":")
    game_id = int(game_id.split()[-1].strip())
    _sets = _sets.split(";")

    sets = []
    for _set in _sets:
        set_dict = {}
        for _type in _set.split(","):
            count, colour = _type.split()
            set_dict[colour.strip()] = int(count.strip())
            sets.append(set_dict)
    return game_id, sets


def main(fpath):
    data = read_data(fpath)
    rules = {"red": 12, "green": 13, "blue": 14}
    ans1 = 0
    ans2 = 0
    for game in data:
        game_id, sets = parse_game(game)
        possible = True
        min_possible = {"red": 0, "green": 0, "blue": 0}
        for _set in sets:
            for colour, count in _set.items():
                if count > rules[colour]:
                    possible = False
                if count > min_possible[colour]:
                    min_possible[colour] = count
        if possible:
            ans1 += game_id
        power = reduce(operator.mul, [v for _, v in min_possible.items()], 1)
        ans2 += power
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys
import statistics
import collections


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(line.strip()) for line in fp.readlines()]
    return data


OPEN = {"{": "}", "(": ")", "<": ">", "[": "]"}
CORRUPT_SCORE = {"}": 1197, ")": 3, ">": 25137, "]": 57}
INCOMPLETE_SCORE = {"}": 3, ")": 1, ">": 4, "]": 2}


def main(fpath):
    data = read_data(fpath)
    corruption_score = 0
    incomplete_scores = []
    stack = collections.deque()
    for line in data:
        incomplete_score = 0
        for symb in line:
            if symb in OPEN:
                stack.append(symb)
            else:
                open_symb = stack.pop()
                if symb != OPEN[open_symb]:
                    corruption_score += CORRUPT_SCORE[symb]
                    stack.clear()
                    break
        for symb in reversed(stack):
            incomplete_score = incomplete_score * 5
            incomplete_score += INCOMPLETE_SCORE[OPEN[symb]]
        if incomplete_score > 0:
            incomplete_scores.append(incomplete_score)
        stack.clear()
    return corruption_score, statistics.median(incomplete_scores)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1, answer_2 = main(fpath)
    print("Answer 1: ", answer_1)
    print("Answer 2: ", answer_2)

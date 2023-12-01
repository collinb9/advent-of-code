import sys
import re


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data

def to_int(number: str):
    map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    res = map.get(number)
    if res is None:
        return int(number)
    return res

def main(fpath):
    data = read_data(fpath)
    expression = r"\d"
    ans1 = []
    for line in data:
        res = list(map(str,re.findall(expression, line)))
        num = int(res[0] + res[-1])
        ans1.append(num)

    expression = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
    ans2 = []
    for line in data:
        res = list(map(str,re.findall(expression, line)))
        num = int(str(to_int(res[0])) + str(to_int(res[-1])))
        ans2.append(num)

    return sum(ans1), sum(ans2)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

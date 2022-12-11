import sys
import operator
import copy


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().split("\n\n")

    monkeys = []
    for monkey in data:
        lines = monkey.split("\n")
        items = [int(i) for i in lines[1].split(":")[-1].strip().split(", ")]
        operation = lines[2].split("=")[-1].strip()
        test = int(lines[3].split(" ")[-1])
        _pass = int(lines[4].split(" ")[-1])
        fail = int(lines[5].split(" ")[-1])
        monkeys.append(
            {
                "items": items,
                "operation": operation,
                "test": test,
                "pass": _pass,
                "fail": fail,
                "inspected": 0,
            }
        )

    return monkeys


def calculate_monkey_business(data, iterations: int, compensate: bool = True):
    common_denominator = 1
    for monkey in data:
        common_denominator *= monkey["test"]
    for _ in range(iterations):
        for monkey in data:
            for item in monkey["items"]:
                worry = eval(monkey["operation"].replace("old", str(item)))
                if compensate:
                    worry = worry // 3
                else:
                    worry = worry % common_denominator
                if worry % monkey["test"] == 0:
                    data[monkey["pass"]]["items"].append(worry)
                else:
                    data[monkey["fail"]]["items"].append(worry)
                monkey["inspected"] += 1
            monkey["items"] = []
    data = sorted(data, key=operator.itemgetter("inspected"), reverse=True)
    return data[0]["inspected"] * data[1]["inspected"]


def main(fpath):
    data = read_data(fpath)
    data2 = copy.deepcopy(data)
    return calculate_monkey_business(
        data, 20, True
    ), calculate_monkey_business(data2, 10000, False)


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

import sys
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def main(fpath):
    data = read_data(fpath)
    cycle = 0
    register = 1
    signal_strength = 0
    message = ["."] * 240
    for item in data:
        _data = item.split(" ")
        instruction = _data[0]
        _range = 1
        if instruction == "addx":
            _range = 2
        for _ in range(_range):
            cycle += 1
            if register <= cycle % 40 <= register + 2:
                message[cycle - 1] = "#"
            if (cycle + 20) % 40 == 0:
                signal_strength += cycle * register
        if instruction == "addx":
            register += int(_data[-1])
    message = " " + " ".join(
        [" ".join(message[i * 40 : i * 40 + 40]) + "\n" for i in range(6)]
    )
    return signal_strength, message


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print(answer2)

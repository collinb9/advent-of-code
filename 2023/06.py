import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def ways_to_win(time, distance):
    ans = 0
    for charge_time in reversed(
        range(int((time + 1) / 2))
    ):  # All times are odd numbers
        if charge_time * (time - charge_time) > distance:
            # Add 2 since the distance calculation is symmetric
            ans += 2
        else:
            return ans


def main(fpath):
    data = read_data(fpath)

    # Part 1
    times = map(int, data[0].split()[1:])
    distances = map(int, data[1].split()[1:])
    ans1 = 1
    for time, distance in zip(times, distances):
        ans1 *= ways_to_win(time, distance)

    # Part 2
    time = int("".join(data[0].split()[1:]))
    distance = int("".join(data[1].split()[1:]))
    ans2 = ways_to_win(time, distance)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

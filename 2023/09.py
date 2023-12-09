import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [
            list(map(int, line.replace("\n", "").split())) for line in fp.readlines()
        ]

    return data


def main(fpath):
    data = read_data(fpath)
    # print(data)
    ans1 = 0
    ans2 = 0
    for history in data:
        diff = history
        differences = []
        while True:
            diff = [diff[i + 1] - diff[i] for i in range(len(diff) - 1)]
            if all(xx == 0 for xx in diff):
                break
            differences.append(diff)
        incnext = 0
        incprev = 0
        while differences:
            diff = differences.pop()
            incnext += diff[-1]
            incprev += diff[0]
            incprev *= -1
        ans1 += history[-1] + incnext
        ans2 += history[0] + incprev

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

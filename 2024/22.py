import sys
import collections


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [int(line) for line in fp.read().splitlines()]

    return data


def mix(value, number):
    return value ^ number


def prune(number):
    return number % 16777216


def evolve(number):
    res = prune(mix(number, number * 64))
    res = prune(mix(res, res // 32))
    res = prune(mix(res, res * 2048))
    return res


def main(fpath):
    data = read_data(fpath)

    ans1 = 0
    ans2 = 0

    change_sequences = collections.defaultdict(int)
    for number in data:
        seen = set()
        prev = number % 10
        prev_4 = collections.deque()
        for ii in range(2000):
            number = evolve(number)
            _number = number % 10
            diff = _number - prev
            prev_4.append(diff)
            if ii > 3:
                prev_4.popleft()
                _seq = tuple(prev_4)
                if _seq not in seen:
                    change_sequences[_seq] += _number
                seen.add(_seq)
            prev = _number

        ans1 += number

    winning_sequence = max(change_sequences, key=change_sequences.get)
    ans2 = change_sequences[winning_sequence]
    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

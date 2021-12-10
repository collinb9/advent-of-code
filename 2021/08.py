import sys
import collections
import itertools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.strip().split("|") for line in fp.readlines()]
    data = [(dat[0].split(), dat[1].split()) for dat in data]
    return data


SINGLES = {2: [1], 3: [7], 4: [4], 7: [8]}

NUMBERS = list(range(10))
SIGNALS = [
    set("abcefg"),
    set("cf"),
    set("acdeg"),
    set("acdfg"),
    set("bcdf"),
    set("abdfg"),
    set("abdfeg"),
    set("acf"),
    set("abcdefg"),
    set("abcdfg"),
]
LETTERS = "abcdefg"


def problem_1(fpath):
    data = read_data(fpath)
    outputs = [dat[1] for dat in data]
    output = list(map(len, itertools.chain.from_iterable(outputs)))
    counter = collections.Counter(output)
    return sum([counter[i] for i in SINGLES.keys()])


def apply_permutation(data, permutation):
    return "".join(tuple(permutation[LETTERS.index(i)] for i in data))


def signal_to_number(signal):
    for num, sig in zip(NUMBERS, SIGNALS):
        if sig == signal:
            return num
    raise ValueError(f"Signal {signal} does not correspond to a number")


def problem_2(fpath):
    """Dirty brute force ..."""
    data = read_data(fpath)
    permutations = list(itertools.permutations(LETTERS))
    answer = []
    for line in data:
        everything = list(itertools.chain.from_iterable(line))
        for perm in permutations:
            transformed = [
                apply_permutation(item, perm) for item in everything
            ]
            if all([set(item) in SIGNALS for item in transformed]):
                answer.append(
                    "".join(
                        [
                            str(signal_to_number(set(out)))
                            for out in transformed[-4:]
                        ]
                    )
                )
                break
        else:
            raise ValueError("No permutation worked")
    return sum(map(int, answer))


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = problem_1(fpath)
    print("Answer 1: ", answer_1)
    answer_2 = problem_2(fpath)
    print("Answer 2: ", answer_2)

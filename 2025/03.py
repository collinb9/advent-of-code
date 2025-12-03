import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()

    return data


def get_max_number(bank, digits=2):
    current = 0
    index = 0
    curr_length = 0
    res = ""
    bank_length = len(bank)
    while curr_length < digits:
        for ii, digit in enumerate(
            bank[index : bank_length - 1 * (digits - curr_length - 1)]
        ):
            _digit = int(digit)
            if _digit > current:
                current = _digit
                _index = ii
        res = f"{res}{current}"
        curr_length += 1
        current = 0
        index = index + _index + 1

    return int(res)


def main(fpath):
    data = read_data(fpath)

    ans1 = 0
    ans2 = 0

    for bank in data:
        ans1 += get_max_number(bank, digits=2)
        ans2 += get_max_number(bank, digits=12)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

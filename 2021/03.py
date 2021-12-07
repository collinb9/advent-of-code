import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [int(line, 2) for line in fp.readlines()]
    return data


def problem_1(fpath):
    data = read_data(fpath)
    gamma = ""
    bit_length = max(data).bit_length()
    for i in reversed(range(bit_length)):
        temp_data = [num % 2 ** (i + 1) >> i for num in data]
        total = sum([num for num in temp_data])
        new_bit = str(int(total > len(data) / 2))
        gamma += new_bit
    gamma = int(gamma, 2)
    epsilon = gamma ^ int((2 ** (bit_length)) - 1)
    return gamma * epsilon


def problem_2(fpath):
    data = read_data(fpath)
    gamma = ""
    bit_length = max(data).bit_length()

    def apply_filter(data, positive: bool):
        data = list(data)
        for i in reversed(range(bit_length)):
            temp_data = [num % 2 ** (i + 1) for num in data]
            current_bits = [num % 2 ** (i + 1) >> i for num in data]
            total = sum(current_bits)
            keep = (total >= len(data) / 2) == positive
            data = [
                num
                for num, temp_num in zip(data, temp_data)
                if (temp_num >= 2 ** (i)) == keep
            ]
            if len(data) == 1:
                oxygen = data[0]
                break
        return oxygen

    oxygen = apply_filter(data, True)
    co2 = apply_filter(data, False)
    return oxygen * co2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = problem_1(fpath)
    print("Answer 1: ", answer_1)
    answer_2 = problem_2(fpath)
    print("Answer 2: ", answer_2)

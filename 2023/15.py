import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "").split(",") for line in fp.readlines()][0]

    return data


def compute_hash(string):
    res = 0
    for char in string:
        res += ord(char)
        res *= 17
        res = res % 256
    return res


def main(fpath):
    data = read_data(fpath)

    # Part 1
    ans1 = sum(map(compute_hash, data))

    # Part 2
    boxes = [[[], []] for _ in range(256)]
    for string in data:
        if "-" in string:
            label = string[:-1]
            focal_length = None
        elif "=" in string:
            operation = "="
            label, focal_length = string.split(operation)
            focal_length = int(focal_length)
        _box = compute_hash(label)
        labels, focal_lengths = boxes[_box]
        if focal_length is None:
            if label in labels:
                _index = labels.index(label)
                labels.pop(_index)
                focal_lengths.pop(_index)
        else:
            if label in labels:
                _index = labels.index(label)
                labels[_index] = label
                focal_lengths[_index] = focal_length

            else:
                labels.append(label)
                focal_lengths.append(focal_length)

    ans2 = 0
    for i, (_, focal_lengths) in enumerate(boxes):
        for j, focal_length in enumerate(focal_lengths):
            ans2 += (i + 1) * ((j + 1) * focal_length)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

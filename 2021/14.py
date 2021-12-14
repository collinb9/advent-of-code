import sys
import collections


def read_data(fpath):
    data = []
    with open(fpath, "r") as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            if not line.strip():
                break
            template = str(line.strip())

        for line in lines[i:]:
            if line.strip():
                data.append(line.strip().split(" -> "))
    return template, data


def main(fpath, steps):
    template, data = read_data(fpath)
    insertions = {dat[0]: dat[1] for dat in data}
    insertion_counter = collections.Counter()
    char_counter = collections.Counter(template)
    previous = ""

    # Initialise the insertion counter from the template
    for tt in list(template):
        if previous + tt in insertions:
            i = insertions[previous + tt]
            char_counter[i] += 1
            ll = previous + i
            rr = i + tt
            if ll in insertions:
                insertion_counter[ll] += 1
            if rr in insertions:
                insertion_counter[rr] += 1
        previous = tt

    # Use the number of occurences of each insertion in one iteration to
    # compute the insertions for the next iteration
    for _ in range(steps - 1):
        next_counter = collections.Counter()
        for k, v in insertion_counter.items():
            ii = insertions[k]
            char_counter[ii] += v
            ll = k[0] + ii
            rr = ii + k[1]
            if ll in insertions:
                next_counter[ll] += v
            if rr in insertions:
                next_counter[rr] += v
        insertion_counter = next_counter

    return char_counter.most_common()[0][1] - char_counter.most_common()[-1][1]


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer_1 = main(fpath, 10)
    print("Answer 1: ", answer_1)
    answer_2 = main(fpath, 40)
    print("Answer 2: ", answer_2)

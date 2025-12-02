import sys

def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [list(map(int, _range.split('-'))) for _range in  fp.read().splitlines()[0].split(',')]

    return data


def check_valid(_id, part=1):
    id_str = str(_id)
    id_str_len = len(id_str)
    if part==1:
        if id_str_len % 2 == 1:
            return True
        elif id_str[:id_str_len//2] == id_str[id_str_len//2:]:
            return False
    elif part == 2:
        for ii in range(1, id_str_len // 2 + 1):
            part = id_str[:ii]
            for jj in range(ii, id_str_len, ii):
                rep_part = id_str[jj: jj+ii]
                if part != rep_part:
                    break
            else:
                return False
        return True
    return True

def check_range(_range, part=1):
    res = 0
    start, end = _range
    if part == 1:
        if len(str(start)) % 2 == 1 and len(str(start)) == len(str(end)):
            return 0
    for _id in range(start, end + 1):
        if not check_valid(_id, part=part):
            res += _id
    return res

def main(fpath):
    data = read_data(fpath)

    ans1 = 0
    ans2 = 0
    for _range in data:
        ans1 += check_range(_range, part=1)
        ans2 += check_range(_range, part=2)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

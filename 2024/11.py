import sys
import functools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = list(map(int, fp.read().split()))

    return data


@functools.lru_cache(maxsize=None)
def blink(stone, count=0, max_count=0):
    if count >= max_count:
        return 1
    if stone == 0:
        return blink(1, count + 1, max_count)
    if len(str(stone)) % 2 == 0:
        stone = str(stone)
        half_len = len(stone) // 2
        return blink(int(stone[:half_len]), count + 1, max_count) + blink(
            int(stone[half_len:]), count + 1, max_count
        )
    return blink(stone * 2024, count + 1, max_count)


def main(fpath):
    stones = read_data(fpath)

    ans1 = 0
    ans2 = 0

    for stone in stones:
        ans1 += blink(stone, 0, 25)
        ans2 += blink(stone, 0, 75)

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

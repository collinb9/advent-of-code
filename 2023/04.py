import sys


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = [line.replace("\n", "") for line in fp.readlines()]

    return data


def count_copies(copies):
    ans = 0

    def inner(card):
        nonlocal ans
        nonlocal copies
        ans += len(copies[card])
        for copy in copies[card]:
            inner(copy)

    for card in copies:
        # Handle original cards
        ans += 1
        inner(card)
    return ans


def main(fpath):
    data = read_data(fpath)
    ans1 = []
    copies = {}
    for card in data:
        # Parsing
        card_number, numbers = card.split(":")
        card_number = int(card_number.split()[-1])
        winners, mine = numbers.split("|")
        winners = set(map(int, winners.split()))
        mine = set(map(int, mine.split()))

        my_winners = winners & mine
        number_of_winners = len(my_winners)
        # copies for part 2, handle overflow on the number of winners
        copies[card_number] = list(
            range(
                card_number + 1, min(len(data) + 2, card_number + number_of_winners + 1)
            )
        )
        if my_winners:
            ans1.append(2 ** (number_of_winners - 1))
    ans2 = count_copies(copies)

    return sum(ans1), ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)

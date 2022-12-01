import requests
import os
import datetime

SESSION_ID = os.environ["SESSION_ID"]


def get_puzzle_input(year: int, day: int):
    resp = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": SESSION_ID},
    )
    resp.raise_for_status()
    outfile = f"./data/{year}/{day:02d}.in"
    with open(outfile, "w+") as fh:
        fh.write(resp.text)
    print(f"Input saved to {outfile}")


if __name__ == "__main__":
    today = datetime.date.today()
    year, day = today.year, today.day
    get_puzzle_input(year, day)

import re
import time
from math import prod
from typing import Dict

from utils import read_data

PILES = re.compile(r"(?P<amount>\d+) (?P<color>red|green|blue)")


class Game:
    max_colors: Dict[str, int]

    def __init__(self, line: str):
        self.max_colors = {"red": 0, "green": 0, "blue": 0}
        for match in PILES.finditer(line):
            color, amount = match.group("color"), int(match.group("amount"))
            self.max_colors[color] = max(self.max_colors[color], amount)

    def is_valid(self) -> bool:
        max_valid = {"red": 12, "green": 13, "blue": 14}
        return all(self.max_colors[x] <= max_valid[x] for x in max_valid)


def main():
    games = [Game(x) for x in read_data().splitlines()]
    # For part 1, we need to do i+1 because game 1 starts on line 0
    print(f"Part one: {sum(i+1 for i, x in enumerate(games) if x.is_valid())}")
    print(f"Part two: {sum(prod(x.max_colors.values()) for x in games)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

import re
import time
from collections import defaultdict
from math import prod

from utils import read_data

PILES = re.compile(r"(?P<amount>\d+) (?P<color>red|green|blue)")


class Game:
    max_colors: defaultdict[str, int]

    def __init__(self, line: str):
        self.max_colors = defaultdict(int)
        for match in PILES.finditer(line):
            self.max_colors[match.group("color")] = max(
                self.max_colors[match.group("color")], int(match.group("amount"))
            )

    def is_valid(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return (
            self.max_colors["red"] <= max_red
            and self.max_colors["green"] <= max_green
            and self.max_colors["blue"] <= max_blue
        )

    def get_power(self) -> int:
        return prod(self.max_colors.values())


def main():
    games = [Game(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(i+1 for i, x in enumerate(games) if x.is_valid(12, 13, 14))}")
    print(f"Part two: {sum(x.get_power() for x in games)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

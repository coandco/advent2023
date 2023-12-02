from typing import List, NamedTuple
from utils import read_data
import time


class Round(NamedTuple):
    red: int = 0
    blue: int = 0
    green: int = 0

    @classmethod
    def from_string(cls, raw_round: str) -> 'Round':
        seen = {}
        for num_and_color in raw_round.split(", "):
            num, color = num_and_color.split(" ")
            seen[color] = int(num)
        return cls(**seen)


class Game:
    game_num: int
    rounds: List[Round]

    def __init__(self, line: str):
        gamenum_str, games_recs = line.split(": ", maxsplit=1)
        self.game_num = gamenum_str.split(" ", maxsplit=1)[1]
        self.rounds = [Round.from_string(x) for x in games_recs.split("; ")]

    def is_valid(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return all(x.red <= max_red and x.blue <= max_blue and x.green <= max_green for x in self.rounds)

    def get_power(self) -> int:
        return max(x.red for x in self.rounds) * max(x.blue for x in self.rounds) * max(x.green for x in self.rounds)


def main():
    games = [Game(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(i+1 for i, x in enumerate(games) if x.is_valid(12, 13, 14))}")
    print(f"Part two: {sum(x.get_power() for x in games)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

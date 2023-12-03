from math import log10
from typing import Dict, List, NamedTuple, Set

from utils import read_data, BaseCoord as Coord
import time


class Number(NamedTuple):
    origin: Coord
    raw_value: str
    value: int

    @staticmethod
    def from_raw(origin: Coord, raw_value: str) -> 'Number':
        return Number(origin=origin, raw_value=raw_value, value=int(raw_value))

    @property
    def self_coords(self) -> Set[Coord]:
        return {Coord(y=self.origin.y, x=self.origin.x+offset) for offset in range(len(self.raw_value))}

    @property
    def neighbors(self):
        return set().union(*(x.neighbors() for x in self.self_coords)) - self.self_coords

    def is_part_number(self, symbols: Dict[Coord, str]):
        return any(x in symbols for x in self.neighbors)


class Schematic:
    board: Dict[Coord, str]
    numbers: Dict[Coord, Number]
    symbols: Dict[Coord, str]

    def __init__(self, lines: List[str]):
        self.board = {}
        self.numbers = {}
        self.symbols = {}
        part_origin = None
        part_raw_value = None
        for y, line in enumerate(lines):
            if part_origin:
                self.numbers[part_origin] = Number.from_raw(part_origin, part_raw_value)
                part_origin = None
                part_raw_value = None
            for x, char in enumerate(line):
                curloc = Coord(y=y, x=x)
                if char != '.':
                    self.board[curloc] = char
                if char.isdigit():
                    if not part_origin:
                        part_origin = curloc
                        # We want part_raw_value to be a copy of the char
                        part_raw_value = char[:]
                    else:
                        part_raw_value += char
                else:
                    if part_origin:
                        self.numbers[part_origin] = Number.from_raw(part_origin, part_raw_value)
                        part_origin = None
                        part_raw_value = None
                    if char != '.':
                        self.symbols[curloc] = char

    def valid_part_nums(self) -> List[int]:
        return [x.value for x in self.numbers.values() if x.is_part_number(self.symbols)]


def main():
    board = Schematic(read_data().splitlines())
    print(f"Part one: {sum(board.valid_part_nums())}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

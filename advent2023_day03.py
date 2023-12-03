import time
from collections import defaultdict
from math import prod
from typing import Dict, List, Set

from utils import BaseCoord as Coord
from utils import read_data


class Schematic:
    numbers: Dict[Coord, str]
    symbols: Dict[Coord, str]
    symbol_neighbors: defaultdict[Coord, Set[Coord]]

    def __init__(self, lines: List[str]):
        self.numbers = {}
        self.symbols = {}
        self.symbol_neighbors = defaultdict(set)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                curloc = Coord(y=y, x=x)
                if char == ".":
                    continue
                elif char.isdigit():
                    self.numbers[curloc] = char
                else:
                    self.symbols[curloc] = char
        for symbol_loc in self.symbols:
            for loc in symbol_loc.neighbors():
                if loc in self.numbers:
                    while loc + Coord(y=0, x=-1) in self.numbers:
                        loc = loc + Coord(y=0, x=-1)
                    self.symbol_neighbors[symbol_loc].add(loc)

    def part_num_origins(self) -> Set[Coord]:
        return set().union(*self.symbol_neighbors.values())

    def gear_locs(self) -> Set[Coord]:
        return {x for x in self.symbols if self.symbols[x] == "*" and len(self.symbol_neighbors[x]) == 2}

    def gear_ratio(self, gear: Coord) -> int:
        return prod(self.read_part_num(x) for x in self.symbol_neighbors[gear])

    def read_part_num(self, origin: Coord) -> int:
        cur_loc = origin
        digits = self.numbers[cur_loc]
        while cur_loc + Coord(y=0, x=1) in self.numbers:
            cur_loc = cur_loc + Coord(y=0, x=1)
            digits += self.numbers[cur_loc]
        return int(digits)


def main():
    board = Schematic(read_data().splitlines())
    print(f"Part one: {sum(board.read_part_num(x) for x in board.part_num_origins())}")
    print(f"Part two: {sum(board.gear_ratio(x) for x in board.gear_locs())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

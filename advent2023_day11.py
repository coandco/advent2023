import time
from itertools import combinations
from typing import Set

from utils import BaseCoord as Coord
from utils import read_data


class Universe:
    galaxy_locs: Set[Coord]

    def __init__(self, raw_universe: str):
        self.galaxy_locs = set()
        for y, line in enumerate(raw_universe.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    self.galaxy_locs.add(Coord(y=y, x=x))

    def __str__(self):
        output = []
        min_x, max_x = min(x.x for x in self.galaxy_locs), max(x.x for x in self.galaxy_locs)
        min_y, max_y = min(x.y for x in self.galaxy_locs), max(x.y for x in self.galaxy_locs)
        for y in range(min_y, max_y + 1):
            line = "".join("#" if Coord(y=y, x=x) in self.galaxy_locs else "." for x in range(min_x, max_x + 1))
            output.append(line)
        return "\n".join(output)

    def expand(self, amount=1):
        min_x, max_x = min(x.x for x in self.galaxy_locs), max(x.x for x in self.galaxy_locs)
        min_y, max_y = min(x.y for x in self.galaxy_locs), max(x.y for x in self.galaxy_locs)

        cur_x = min_x
        while cur_x <= max_x:
            if any(x.x == cur_x for x in self.galaxy_locs):
                cur_x += 1
            else:
                affected_galaxies = {x for x in self.galaxy_locs if x.x > cur_x}
                self.galaxy_locs -= affected_galaxies
                adjusted_galaxies = {Coord(x=x.x + amount, y=x.y) for x in affected_galaxies}
                self.galaxy_locs |= adjusted_galaxies
                max_x += amount
                cur_x += amount + 1

        cur_y = min_y
        while cur_y <= max_y:
            if any(x.y == cur_y for x in self.galaxy_locs):
                cur_y += 1
            else:
                affected_galaxies = {x for x in self.galaxy_locs if x.y > cur_y}
                self.galaxy_locs -= affected_galaxies
                adjusted_galaxies = {Coord(x=x.x, y=x.y + amount) for x in affected_galaxies}
                self.galaxy_locs |= adjusted_galaxies
                max_y += amount
                cur_y += amount + 1

    def shortest_paths(self) -> int:
        total_length = 0
        for first, second in combinations(self.galaxy_locs, 2):
            total_length += first.distance(second)
        return total_length


def main():
    universe = Universe(read_data())
    universe.expand(amount=1)
    print(f"Part one: {universe.shortest_paths()}")
    # We've already replaced each 1 with 2, so now replace each of those 2 with 500k
    universe.expand(amount=(1_000_000 // 2) - 1)
    print(f"Part two: {universe.shortest_paths()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

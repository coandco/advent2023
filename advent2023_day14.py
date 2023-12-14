from typing import Set, Optional, FrozenSet

from utils import read_data, BaseCoord as Coord
import time

DIRECTIONS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}


class Platform:
    walls: Set[Coord]
    initial_rocks: Set[Coord]
    rocks: Set[Coord]
    max_x: int
    max_y: int

    def __init__(self, raw_field: str):
        self.walls, self.rocks = set(), set()
        lines = raw_field.splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    self.walls.add(Coord(y=y, x=x))
                elif char == "O":
                    self.rocks.add(Coord(y=y, x=x))
        self.initial_rocks = self.rocks.copy()
        self.max_x = len(lines[0])
        self.max_y = len(lines)

    def __str__(self, rock_locs: Optional[FrozenSet[Coord]] = None) -> str:
        rock_locs = rock_locs or self.rocks
        output = []
        for y in range(self.max_y):
            # WTF Pycharm https://youtrack.jetbrains.com/issue/PY-30598
            line = [" "]
            for x in range(self.max_x):
                curloc = Coord(y=y, x=x)
                if curloc in self.walls:
                    line.append("#")
                elif curloc in rock_locs:
                    line.append("O")
                else:
                    line.append(".")
            output.append("".join(line))
        return "\n".join(output)

    def reset(self):
        self.rocks = self.initial_rocks.copy()

    def in_bounds(self, coord: Coord) -> bool:
        return 0 <= coord.x < self.max_x and 0 <= coord.y < self.max_y

    def roll_one(self, rock: Coord, direction: str):
        new_pos = rock
        while True:
            to_test = new_pos + DIRECTIONS[direction]
            if (not self.in_bounds(to_test)) or to_test in self.walls or to_test in self.rocks:
                break
            new_pos = to_test
        if new_pos != rock:
            self.rocks.remove(rock)
            self.rocks.add(new_pos)

    def roll(self, direction: str):
        raw_dir = DIRECTIONS[direction]

        for rock in sorted(self.rocks, key=lambda x: x.x * raw_dir.x if raw_dir.x else x.y * raw_dir.y, reverse=True):
            self.roll_one(rock, direction)

    def spin_cycle(self, num_cycles: int):
        # Each cycle is one N/W/S/E combo
        num_cycles *= 4
        seen = [frozenset(self.rocks)]
        offset = None
        while not offset:
            for direction in ('N', 'W', 'S', 'E'):
                self.roll(direction)
                rock_state = frozenset(self.rocks)
                if rock_state in seen:
                    offset = seen.index(rock_state)
                    break
                seen.append(rock_state)
        if num_cycles < offset:
            return self.score(seen[num_cycles])
        cycle_length = len(seen) - offset
        final_state = seen[offset + ((num_cycles - offset) % cycle_length)]
        return self.score(final_state)

    def score(self, to_score: Optional[FrozenSet[Coord]] = None):
        to_score = to_score or self.rocks
        return sum(self.max_y - x.y for x in to_score)


def main():
    platform = Platform(read_data())
    platform.roll('N')
    print(f"Part one: {platform.score()}")
    platform.reset()
    print(f"Part two: {platform.spin_cycle(1000000000)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

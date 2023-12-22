import time
from typing import List, Optional, Set, Tuple

from utils import BaseCoord as Coord
from utils import read_data


# Adapted from https://pythonhint.com/post/1131993020348204/lagrange-interpolation-in-python
def lagrange_interpolation(data_points: List[int], multiple) -> int:
    # Initialize the result variable
    result = 0

    for i in range(len(data_points)):
        # Calculate the Lagrange basis polynomial
        term = 1
        for j in range(len(data_points)):
            if j != i:
                term *= (multiple - j) / (i - j)

        # Add the contribution of the current data point to the result
        result += data_points[i] * term

    return int(result)


class Garden:
    walls: Set[Coord]
    start_loc: Coord
    max_x: int
    max_y: int

    def __init__(self, raw_garden: str):
        self.walls = set()
        lines = raw_garden.splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    self.walls.add(Coord(x=x, y=y))
                elif char == "S":
                    self.start_loc = Coord(x=x, y=y)
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def point_valid(self, coord: Coord) -> bool:
        return not (coord.y % self.max_y, coord.x % self.max_x) in self.walls

    def points_of_interest(
        self, steps: List[int], start: int = 0, state: Optional[Set[Coord]] = None
    ) -> Tuple[List[int], Set[Coord]]:
        values = []
        state = state if state else {self.start_loc}
        for i in range(start, max(steps) + 1):
            if i in steps:
                values.append(len(state))
            new_state = set()
            for loc in state:
                new_state |= {x for x in loc.cardinal_neighbors() if self.point_valid(x)}
            state = new_state
        return values, state


def main():
    garden = Garden(read_data())
    part_one, state = garden.points_of_interest([64])
    print(f"Part one: {part_one[0]}")
    # For part two, we start in the middle of the board, and there are 65 squares to the edge
    # The board then repeats every 131 squares, so we want to sample at the beginning of our first three repeats
    part_two, _ = garden.points_of_interest(
        [garden.start_loc.x + (n * garden.max_x) for n in range(3)], start=65, state=state
    )
    # The input is a square, and the given number of steps places us exactly at a boundary evenly divisible by
    # our repeat width (131 squares) after going to the first edge
    cycles = (26501365 - garden.start_loc.x) // garden.max_x
    print(f"Part two: {lagrange_interpolation(part_two, cycles)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

from math import prod
from typing import Set, List, Tuple, Dict

from utils import read_data, BaseCoord as Coord
import time


DIRECTIONS = {"U": Coord(x=0, y=-1), "R": Coord(x=1, y=0), "D": Coord(x=0, y=1), "L": Coord(x=-1, y=0)}
NUM_DIRECTIONS = {"3": Coord(x=0, y=-1), "0": Coord(x=1, y=0), "1": Coord(x=0, y=1), "2": Coord(x=-1, y=0)}


# Black magic adapted from https://www.101computing.net/the-shoelace-algorithm/
def shoelace_area(vertices: List[Coord], wall_area: int):
    num_v = len(vertices)
    sum1 = sum(vertices[i].x * vertices[(i + 1) % num_v].y for i in range(num_v))
    sum2 = sum(vertices[i].y * vertices[(i + 1) % num_v].x for i in range(num_v))
    return abs(sum1 - sum2) // 2 + wall_area // 2 + 1


class Trench:
    vertices: List[Coord]
    hex_vertices: List[Coord]
    wall_area: int
    hex_wall_area: int

    def __init__(self, raw_field: str):
        self.vertices = []
        self.hex_vertices = []
        self.wall_area = self.hex_wall_area = 0
        curloc = hex_curloc = Coord(0, 0)
        for line in raw_field.splitlines():
            raw_heading, raw_distance, raw_color = line.split()
            # Handle part 1 instructions
            distance = int(raw_distance)
            displacement = DIRECTIONS[raw_heading] * distance
            self.wall_area += distance
            curloc += displacement
            self.vertices.append(curloc)

            # Handle part 2 instructions
            distance = int(raw_color[2:-2], base=16)
            displacement = NUM_DIRECTIONS[raw_color[-2]] * distance
            self.hex_wall_area += distance
            hex_curloc += displacement
            self.hex_vertices.append(hex_curloc)


def main():
    trench = Trench(read_data())
    print(f"Part one: {shoelace_area(trench.vertices, trench.wall_area)}")
    print(f"Part two: {shoelace_area(trench.hex_vertices, trench.hex_wall_area)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

import heapq
import time
from itertools import accumulate
from typing import Dict, Iterator, Tuple

from utils import BaseCoord as Coord
from utils import read_data

DIRECTIONS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}
RIGHT_TURNS = {"N": "E", "E": "S", "S": "W", "W": "N"}
LEFT_TURNS = {"N": "W", "E": "N", "S": "E", "W": "S"}
VALID_DIRECTIONS = {"N": {"N", "W", "E"}, "E": {"E", "N", "S"}, "S": {"S", "W", "E"}, "W": {"W", "N", "S"}}


class HeatMap:
    map: Dict[Coord, int]

    def __init__(self, raw_map):
        lines = raw_map.splitlines()
        self.map = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self.map[Coord(x=x, y=y)] = int(char)
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def in_bounds(self, coord: Coord) -> bool:
        return coord.x in range(self.max_x) and coord.y in range(self.max_y)

    def walk_direction(self, coord: Coord, heading: str, min_move: int, max_move: int) -> Iterator[Tuple[Coord, int]]:
        extra_cost = 0
        # Need to start at one to accumulate total cost
        for i in range(1, max_move + 1):
            coord += DIRECTIONS[heading]
            if not self.in_bounds(coord):
                break
            extra_cost += self.map[coord]
            # Now that we've accumulated the heat loss, apply the min move setting
            if i < min_move:
                continue
            yield extra_cost, coord

    def find_min_path(self, min_move: int = 0, max_move: int = 3) -> int:
        # We need to avoid loops
        seen = set()
        # cost, curloc, last_dir
        heap = [(0, Coord(0, 0), "E"), (0, Coord(0, 0), "S")]
        destination = Coord(y=self.max_y - 1, x=self.max_x - 1)
        while heap:
            cost, curloc, last_dir = heapq.heappop(heap)
            if curloc == destination:
                return cost
            if (curloc, last_dir) in seen:
                continue
            seen.add((curloc, last_dir))
            for heading in (RIGHT_TURNS[last_dir], LEFT_TURNS[last_dir]):
                for extra_cost, new_loc in self.walk_direction(curloc, heading, min_move, max_move):
                    heapq.heappush(heap, (cost + extra_cost, new_loc, heading))


def main():
    heatmap = HeatMap(read_data())
    print(f"Part one: {heatmap.find_min_path(max_move=3)}")
    print(f"Part two: {heatmap.find_min_path(min_move=4, max_move=10)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

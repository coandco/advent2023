import heapq
import time
from itertools import accumulate
from typing import Dict

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

    def find_min_path(self, min_move: int = 0, max_move: int = 3) -> int:
        # We need to avoid loops
        seen = set()
        # heat_loss, curloc, last_dir
        heap = [(0, Coord(0, 0), "E"), (0, Coord(0, 0), "S")]
        destination = Coord(y=self.max_y - 1, x=self.max_x - 1)
        while heap:
            heat_loss, curloc, last_dir = heapq.heappop(heap)
            if curloc == destination:
                return heat_loss
            if (curloc, last_dir) in seen:
                continue
            seen.add((curloc, last_dir))
            for heading in (RIGHT_TURNS[last_dir], LEFT_TURNS[last_dir]):
                new_heat_loss = heat_loss
                new_loc = curloc
                # Need to start at one to accumulate total cost
                for i in range(1, max_move + 1):
                    new_loc += DIRECTIONS[heading]
                    if not self.in_bounds(new_loc):
                        break
                    new_heat_loss += self.map[new_loc]
                    # Now that we've accumulated the heat loss, apply the min move setting
                    if i < min_move:
                        continue
                    heapq.heappush(heap, (new_heat_loss, new_loc, heading))


def main():
    heatmap = HeatMap(read_data())
    print(f"Part one: {heatmap.find_min_path(max_move=3)}")
    print(f"Part two: {heatmap.find_min_path(min_move=4, max_move=10)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

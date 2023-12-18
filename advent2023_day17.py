import heapq
import sys
import time
from collections import deque, defaultdict
from typing import List, Optional, Dict, Union, Set, Iterable

from utils import BaseCoord as Coord
from utils import read_data

DIRECTIONS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}
RIGHT_TURNS = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
LEFT_TURNS = {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'}
VALID_DIRECTIONS = {'N': {'N', 'W', 'E'}, 'E': {'E', 'N', 'S'}, 'S': {'S', 'W', 'E'}, 'W': {'W', 'N', 'S'}}


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
        return 0 <= coord.x < self.max_x and 0 <= coord.y < self.max_y

    def find_min_path(self, min_move: int = 0, max_move: int = 3) -> int:
        # We need to avoid loops
        seen = set()
        heap = []
        destination = Coord(y=self.max_y-1, x=self.max_x-1)
        # heat_loss, curloc, last_dir, run_length
        heapq.heappush(heap, (0, Coord(0, 0), 'E', 0))
        while heap:
            heat_loss, curloc, last_dir, run_length = heapq.heappop(heap)
            if (curloc, last_dir, run_length) in seen:
                continue
            seen.add((curloc, last_dir, run_length))
            for heading in VALID_DIRECTIONS[last_dir]:
                if curloc == destination:
                    return heat_loss
                if run_length < min_move and heading != last_dir:
                    continue
                if run_length >= max_move and heading == last_dir:
                    continue
                new_loc: Coord = curloc + DIRECTIONS[heading]
                if not self.in_bounds(new_loc):
                    continue
                new_run_length: int = run_length + 1 if heading == last_dir else 1
                heapq.heappush(heap, (heat_loss + self.map[new_loc], new_loc, heading, new_run_length))


def main():
    heatmap = HeatMap(read_data())
    print(f"Part one: {heatmap.find_min_path(max_move=3)}")
    print(f"Part two: {heatmap.find_min_path(min_move=4, max_move=10)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

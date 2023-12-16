from collections import defaultdict
from typing import Dict, Set, Tuple

from utils import read_data, BaseCoord as Coord
import time

DIRECTIONS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}
NEW_DIRECTIONS = {
    "/": {"N": ["E"], "E": ["N"], "S": ["W"], "W": ["S"]},
    "\\": {"N": ["W"], "E": ["S"], "S": ["E"], "W": ["N"]},
    "-": {"N": ["E", "W"], "E": ["E"], "S": ["E", "W"], "W": ["W"]},
    "|": {"N": ["N"], "E": ["N", "S"], "S": ["S"], "W": ["N", "S"]},
    ".": {"N": ["N"], "E": ["E"], "S": ["S"], "W": ["W"]},
}


class MirrorMirror:
    mirrors: Dict[Coord, str]
    max_x: int
    max_y: int

    def __init__(self, raw_field: str):
        self.mirrors = {}
        lines = raw_field.splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != ".":
                    self.mirrors[Coord(y=y, x=x)] = char
        self.max_y = len(lines)
        self.max_x = len(lines[0])

    def __str__(self, highlight=None):
        output = []
        for y in range(self.max_y):
            line = "".join(
                "X" if Coord(y=y, x=x) == highlight else self.mirrors.get(Coord(y=y, x=x), ".")
                for x in range(self.max_x)
            )
            output.append(line)
        return "\n".join(output)

    def in_bounds(self, coord: Coord) -> bool:
        return 0 <= coord.x < self.max_x and 0 <= coord.y < self.max_y

    def find_activated(self, start: Tuple[Coord, str] = (Coord(0, 0), "E")) -> int:
        activated_squares: Set[Coord] = set()
        seen_paths: Dict[Coord, Set[str]] = defaultdict(set)
        queue = [start]
        while queue:
            curloc, curdir = queue.pop()
            mirror_char = self.mirrors.get(curloc, ".")
            if curdir in seen_paths[curloc] or not self.in_bounds(curloc):
                continue
            seen_paths[curloc].add(curdir)
            activated_squares.add(curloc)
            for new_dir in NEW_DIRECTIONS[mirror_char][curdir]:
                queue.append((curloc + DIRECTIONS[new_dir], new_dir))
        return len(activated_squares)

    def align_beam(self) -> int:
        starts = (
            [(Coord(x=0, y=i), "E") for i in range(self.max_y)]
            + [(Coord(x=self.max_x - 1, y=i), "W") for i in range(self.max_y)]
            + [(Coord(x=i, y=0), "S") for i in range(self.max_x)]
            + [(Coord(x=i, y=self.max_y - 1), "N") for i in range(self.max_x)]
        )
        return max(self.find_activated(start=x) for x in starts)


def main():
    mirrors = MirrorMirror(read_data())
    print(f"Part one: {mirrors.find_activated()}")
    print(f"Part two: {mirrors.align_beam()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

from typing import Set, Tuple, Iterator, Optional, List

from utils import read_data, BaseCoord as Coord
import time


class Pattern:
    field: Set[Coord]
    columns: List[Set[int]]
    rows: List[Set[int]]
    max_x: int
    max_y: int

    def __init__(self, raw_field: str):
        self.field = set()
        lines = raw_field.splitlines()
        self.max_x = len(lines[0])
        self.max_y = len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    self.field.add(Coord(y=y, x=x))

        self.columns = [{x.y for x in self.field if x.x == i} for i in range(self.max_x)]
        self.rows = [{x.x for x in self.field if x.y == i} for i in range(self.max_y)]

    def __str__(self):
        output = []
        for y in range(self.max_y+1):
            line = "".join("#" if Coord(y=y, x=x) in self.field else "." for x in range(self.max_x+1))
            output.append(line)
        return "\n".join(output)

    def matching_columns(self, i: int) -> Iterator[Tuple[int, int]]:
        image = i
        reflection = i - 1
        while 0 <= image < self.max_x and 0 <= reflection < self.max_x:
            yield image, reflection
            image += 1
            reflection -= 1

    def matching_rows(self, i: int) -> Iterator[Tuple[int, int]]:
        image = i
        reflection = i - 1
        while 0 <= image < self.max_y and 0 <= reflection < self.max_y:
            yield image, reflection
            image += 1
            reflection -= 1

    def find_mirror(self, old_line: Optional[int] = None) -> Optional[int]:
        # Check for vertical reflections
        for i in range(1, self.max_x):
            for image, reflection in self.matching_columns(i):
                if self.columns[image] != self.columns[reflection]:
                    break
            else:
                if i != old_line:
                    return i
        # Check for horizontal reflections
        for i in range(1, self.max_y):
            for image, reflection in self.matching_rows(i):
                if self.rows[image] != self.rows[reflection]:
                    break
            else:
                if i * 100 != old_line:
                    return i * 100
        return None

    def toggle_coord(self, coord: Coord):
        if coord.y in self.columns[coord.x]:
            self.columns[coord.x].remove(coord.y)
        else:
            self.columns[coord.x].add(coord.y)

        if coord.x in self.rows[coord.y]:
            self.rows[coord.y].remove(coord.x)
        else:
            self.rows[coord.y].add(coord.x)

    def smudge_walk(self, old_line: int) -> int:
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.toggle_coord(Coord(x=x, y=y))
                if found := self.find_mirror(old_line=old_line):
                    return found
                self.toggle_coord(Coord(x=x, y=y))


def main():
    patterns = [Pattern(x) for x in read_data().split("\n\n")]
    mirror_lines = [x.find_mirror() for x in patterns]
    print(f"Part one: {sum(mirror_lines)}")
    print(f"Part two: {sum(x.smudge_walk(mirror_lines[i]) for i, x in enumerate(patterns))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

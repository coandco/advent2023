from typing import Dict, Union, Set

from utils import read_data, BaseCoord as Coord
import time

REPLACEMENTS = {"F": "┌", "7": "┐", "J": "┘", "L": "└"}
DIRECTIONS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}
REAL_START_CHAR = {("N", "E"): "└", ("E", "S"): "┌", ("S", "W"): "┐", ("W", "N"): "┘"}
TURNS = {
    "R": {"N": "E", "E": "S", "S": "W", "W": "N"},
    "L": {"N": "W", "W": "S", "S": "E", "E": "N"},
    "S": {"N": "N", "E": "E", "S": "S", "W": "W"},
}
CONNECTIONS = {
    "N": {"┌": "R", "┐": "L", "|": "S"},
    "E": {"┐": "R", "┘": "L", "-": "S"},
    "S": {"┘": "R", "└": "L", "|": "S"},
    "W": {"└": "R", "┌": "L", "-": "S"},
}


class PipeDream:
    points: Dict[Coord, str]
    start_loc: Coord

    def __init__(self, raw_field: str):
        self.points = {}
        for y, line in enumerate(raw_field.splitlines()):
            line = line.translate(str.maketrans(REPLACEMENTS))
            for x, char in enumerate(line):
                curloc = Coord(y=y, x=x)
                if char == "S":
                    self.start_loc = curloc
                self.points[Coord(y=y, x=x)] = char

    def __str__(self, highlight: Union[Coord, Set[Coord], None] = None) -> str:
        if highlight is None:
            highlight = set()
        if isinstance(highlight, Coord):
            highlight = {highlight}

        output = []
        for y in range(max(x.y for x in self.points) + 1):
            line = "".join(
                "X" if Coord(y=y, x=x) in highlight else self.points.get(Coord(y=y, x=x), ".")
                for x in range(max(x.x for x in self.points) + 1)
            )
            output.append(line)
        return "\n".join(output)

    def winnow(self) -> int:
        curloc = self.start_loc
        valid_headings = [x for x in DIRECTIONS if self.points.get(curloc + DIRECTIONS[x], ".") in CONNECTIONS[x]]
        assert len(valid_headings) == 2, f"Invalid number of connections found from starting loc"
        main_loop = {curloc: REAL_START_CHAR[tuple(valid_headings)]}
        heading = valid_headings[0]
        curloc += DIRECTIONS[heading]
        while curloc != self.start_loc:
            # When we're following the main loop, we should always have a valid connection
            assert self.points[curloc] in CONNECTIONS[heading]
            main_loop[curloc] = self.points[curloc]
            turn_direction = CONNECTIONS[heading][self.points[curloc]]
            heading = TURNS[turn_direction][heading]
            curloc += DIRECTIONS[heading]
        self.points = main_loop
        return len(main_loop) // 2

    def num_enclosed(self) -> int:
        # find_enclosed() assumes self.winnow() has already been run
        enclosed_points = set()

        # Start with a westmost pipe heading north.  By definition, the inside is to the east.
        min_x = min(x.x for x in self.points)
        start = curloc = next(x for x in self.points if x.x == min_x and self.points[x] != "└")
        heading = "N"
        inner_heading = "E"

        # Manually process the start point we picked, checking it for an adjacent interior square
        if curloc + DIRECTIONS[inner_heading] not in self.points:
            enclosed_points.add(curloc + DIRECTIONS[inner_heading])
        turn_direction = CONNECTIONS[heading][self.points[curloc]]
        heading = TURNS[turn_direction][heading]
        inner_heading = TURNS[turn_direction][inner_heading]
        curloc += DIRECTIONS[heading]
        # Go around the loop, adding any non-occupied squares in the inside direction to our set of enclosed points
        while curloc != start:
            if curloc + DIRECTIONS[inner_heading] not in self.points:
                enclosed_points.add(curloc + DIRECTIONS[inner_heading])
            turn_direction = CONNECTIONS[heading][self.points[curloc]]
            heading = TURNS[turn_direction][heading]
            inner_heading = TURNS[turn_direction][inner_heading]
            # When we go around a corner, we need to check both inside neighbors
            if curloc + DIRECTIONS[inner_heading] not in self.points:
                enclosed_points.add(curloc + DIRECTIONS[inner_heading])
            curloc += DIRECTIONS[heading]

        # At this point, we've marked all enclosed points next to walls, so we just need to flood fill
        queue = list(enclosed_points)
        while queue:
            curloc = queue.pop()
            for neighbor in curloc.cardinal_neighbors():
                if not any(neighbor in x for x in (enclosed_points, self.points)):
                    enclosed_points.add(neighbor)
                    queue.append(neighbor)
        return len(enclosed_points)


def main():
    field = PipeDream(read_data())
    print(f"Part one: {field.winnow()}")
    print(f"Part two: {field.num_enclosed()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

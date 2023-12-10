from typing import FrozenSet, Dict, List, Tuple

from utils import read_data, BaseCoord as Coord, CARDINAL_NEIGHBORS_2D
import time

REPLACEMENTS = {"F": "┌", "7": "┐", "J": "┘", "L": "└"}
CONNECTIONS = {
    Coord(x=1, y=0): {"┐": Coord(x=0, y=1), "┘": Coord(x=0, y=-1), "-": Coord(x=1, y=0)},
    Coord(x=-1, y=0): {"┌": Coord(x=0, y=1), "└": Coord(x=0, y=-1), "-": Coord(x=-1, y=0)},
    Coord(x=0, y=1): {"┘": Coord(x=-1, y=0), "└": Coord(x=1, y=0), "|": Coord(x=0, y=1)},
    Coord(x=0, y=-1): {"┌": Coord(x=1, y=0), "┐": Coord(x=-1, y=0), "|": Coord(x=0, y=-1)},
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

    def __str__(self, highlight: Coord = Coord(x=10000, y=10000)) -> str:
        output = []
        for y in range(max(x.y for x in self.points) + 1):
            line = "".join(
                "X" if Coord(y=y, x=x) == highlight else self.points.get(Coord(y=y, x=x), " ")
                for x in range(max(x.x for x in self.points) + 1)
            )
            output.append(line)
        return "\n".join(output)

    def print_field(self):
        print(self.field_as_str())

    def winnow(self) -> int:
        main_loop = {self.start_loc: self.points[self.start_loc]}
        steps = [self.start_loc]

        for heading in CARDINAL_NEIGHBORS_2D:
            if self.points.get(steps[-1] + heading, '.') in CONNECTIONS[heading]:
                steps.append(steps[-1] + heading)
                break
        else:
            raise Exception("No valid connections found from starting loc")
        while steps[-1] != self.start_loc:
            # When we're following the main loop, we should always have a valid connection
            assert self.points[steps[-1]] in CONNECTIONS[heading]
            main_loop[steps[-1]] = self.points[steps[-1]]
            heading = CONNECTIONS[heading][self.points[steps[-1]]]
            steps.append(steps[-1] + heading)
        self.points = main_loop
        return len(steps) // 2


def main():
    field = PipeDream(read_data())
    print(f"Part one: {field.winnow()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

from typing import Set, Dict, NamedTuple, Tuple, Optional, Iterable, FrozenSet

from utils import read_data, BaseCoord as Coord
import time

DIRS: Dict[str, Coord] = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}
RIGHT: Dict[str, str] = {"N": "E", "E": "S", "S": "W", "W": "N"}
LEFT: Dict[str, str] = {"N": "W", "E": "N", "S": "E", "W": "S"}


class Segment(NamedTuple):
    origin: Coord
    length: int
    next: Tuple[Coord, ...]


class Node:
    coord: Coord
    connections: Dict[str, Optional[Coord]]
    distances: Dict[Coord, int]

    def __init__(self, coord: Coord):
        self.coord = coord
        self.connections = {}
        self.distances = {}

    def add_connection(self, heading: str, coord: Coord, length: int):
        self.connections[heading] = coord
        self.distances[coord] = length

    def block_connection(self, heading: str):
        self.connections[heading] = None

    def remaining_dirs(self) -> Iterable[str]:
        yield from (x for x in ('N', 'E', 'S', 'W') if x not in self.connections)

    def connection_lengths(self, valid_dirs: Tuple[str, ...]) -> Dict[Coord, int]:
        return {v: self.distances[v] for k, v in self.connections.items() if v is not None and k in valid_dirs}


class Hike:
    walls: Set[Coord]
    slopes: Dict[Coord, str]
    start: Coord
    end: Coord
    max_x: int
    max_y: int
    valid_exits: Tuple[str, ...] = ('E', 'S')
    nodes: Dict[Coord, Node]

    def __init__(self, raw_hike: str):
        self.walls = set()
        self.slopes = {}
        lines = raw_hike.splitlines()
        self.max_y = len(lines)
        self.max_x = len(lines[0])
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.walls.add(Coord(x=x, y=y))
                elif char in ('^', '>', 'v', '<'):
                    self.slopes[Coord(x=x, y=y)] = char
                elif char == '.' and y == 0:
                    self.start = Coord(x=x, y=y)
                elif char == '.' and y == len(lines) - 1:
                    self.end = Coord(x=x, y=y)
        self.build_nodes()

    def __str__(self, highlight: Optional[Set[Coord]] = None):
        highlight = highlight if highlight else set()
        output = []
        for y in range(self.max_y):
            line = []
            for x in range(self.max_x):
                if (y, x) in highlight:
                    line.append("X")
                elif (y, x) in self.walls:
                    line.append("#")
                elif (y, x) in self.slopes:
                    line.append(self.slopes[Coord(y, x)])
                else:
                    line.append(".")
            output.append("".join(line))
        return "\n".join(output)

    def follow_segment(self, start_loc: Coord, start_dir: str) -> Tuple[Coord, int, str]:
        curloc = start_loc
        curdir = start_dir
        curlength = 1
        while True:
            newloc = curloc + DIRS[curdir]
            # If we've hit the end, we're done
            if newloc == self.end:
                return newloc, curlength, curdir
            # Turn left or right when you hit a wall.  Given our input, only one is valid
            if newloc in self.walls:
                if any(newdir := x for x in (RIGHT[curdir], LEFT[curdir]) if curloc + DIRS[x] not in self.walls):
                    curdir = newdir
                    continue
                else:
                    raise Exception("Shouldn't ever hit this -- dead end!")
            # If we're about to hit an intersection, we're done
            if newloc in self.slopes:
                intersection = newloc + DIRS[curdir]
                curlength += 1
                return intersection, curlength, curdir
            # Otherwise, just keep going straight
            curloc += DIRS[curdir]
            curlength += 1

    def build_nodes(self):
        self.nodes = {}
        queue = [self.start]
        while queue:
            curloc = queue.pop()
            # print(self.__str__(highlight=curloc))
            # print("-------")
            for heading in self.nodes.setdefault(curloc, Node(curloc)).remaining_dirs():
                newloc = curloc + DIRS[heading]
                if newloc.y in range(self.max_y) and newloc not in self.walls:
                    end, length, end_dir = self.follow_segment(newloc, heading)
                    self.nodes.setdefault(curloc, Node(curloc)).add_connection(heading, end, length)
                    self.nodes.setdefault(end, Node(end)).add_connection(RIGHT[RIGHT[heading]], curloc, length)
                    queue.append(end)

    def _max_node_distance(self, coord: Coord, curlength: int, seen: FrozenSet[Coord]) -> int:
        if coord == self.end:
            return curlength
        longest = 0
        for other, seg_length in self.nodes[coord].connection_lengths(self.valid_exits).items():
            if other in seen:
                continue
            longest = max(longest, self._max_node_distance(other, curlength + seg_length + 1, seen | {coord}))
        return longest

    def max_node_distance(self) -> int:
        return self._max_node_distance(self.start, 0, frozenset())


def main():
    TEST = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    hike = Hike(read_data())
    print(f"Part one: {hike.max_node_distance()}")
    hike.valid_exits = ('N', 'E', 'S', 'W')
    print(f"Part two: {hike.max_node_distance()}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

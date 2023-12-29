from itertools import combinations
from typing import Tuple, NamedTuple, Optional

from utils import read_data, BaseCoord, BaseCoord3D as Coord3D
import time, re

DIGITS = re.compile(r'[0-9-]+')

TEST_RANGE = range(7, 27+1)
REAL_RANGE = range(200_000_000_000_000, 400_000_000_000_000+1)


class Coord(BaseCoord):
    def in_range(self, to_check: range) -> bool:
        return self.x in to_check and self.y in to_check


class Hailstone2D(NamedTuple):
    pos: Coord
    vel: Coord

    # adapted from https://stackoverflow.com/a/20677983
    def intersection(self, other: 'Hailstone2D') -> Optional[Coord]:
        # Quick alias to get the determinant of a matrix
        def det(a: Coord, b: Coord) -> int:
            return a.x * b.y - a.y * b.x

        # Quick alias to get the sign of an int
        def sign(num: int) -> int:
            return -1 if num < 0 else 1

        xdiff = Coord(x=self.vel.x, y=other.vel.x)
        ydiff = Coord(x=self.vel.y, y=other.vel.y)
        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = Coord(x=det(self.pos, self.pos - self.vel), y=det(other.pos, other.pos - other.vel))
        x = int(det(d, xdiff) / div)
        y = int(det(d, ydiff) / div)

        for stone in (self, other):
            diff_x, diff_y = x - stone.pos.x, y - stone.pos.y
            if sign(diff_x) != sign(stone.vel.x) or sign(diff_y) != sign(stone.vel.y):
                return None

        # Something about the way I did this gave the inverse of the correct answer
        return Coord(x=x, y=y)


class Hailstone3D(NamedTuple):
    pos: Coord3D
    vel: Coord3D

    @staticmethod
    def from_str(line: str) -> 'Hailstone3D':
        x, y, z, dx, dy, dz = (int(x) for x in DIGITS.findall(line))
        return Hailstone3D(pos=Coord3D(x=x, y=y, z=z), vel=Coord3D(x=dx, y=dy, z=dz))

    def demote(self) -> Hailstone2D:
        return Hailstone2D(pos=Coord(x=self.pos.x, y=self.pos.y), vel=Coord(x=self.vel.x, y=self.vel.y))


def main():
    TEST = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    my_range = REAL_RANGE
    hailstones = [Hailstone3D.from_str(x) for x in read_data().splitlines()]
    hail_2d = [x.demote() for x in hailstones]
    crossing = [1 for i, j in combinations(hail_2d, 2) if (inter := i.intersection(j)) and inter.in_range(my_range)]
    print(f"Part one: {len(crossing)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

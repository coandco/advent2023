import re
import sys
import time
from itertools import combinations
from typing import Iterable, List, NamedTuple, Optional

from utils import BaseCoord
from utils import BaseCoord3D as Coord3D
from utils import read_data

DIGITS = re.compile(r"[0-9-]+")
TEST_RANGE = range(7, 27 + 1)
REAL_RANGE = range(200_000_000_000_000, 400_000_000_000_000 + 1)


class Coord(BaseCoord):
    def in_range(self, to_check: range) -> bool:
        return self.x in to_check and self.y in to_check


class Hailstone2D(NamedTuple):
    pos: Coord
    vel: Coord

    # adapted from https://stackoverflow.com/a/20677983
    def intersection(self, other: "Hailstone2D", dv: Optional[Coord] = None) -> Optional[Coord]:
        # Quick alias to get the determinant of a matrix
        def det(a: Coord, b: Coord) -> int:
            return a.x * b.y - a.y * b.x

        # Quick alias to get the sign of an int
        def sign(num: int) -> int:
            return -1 if num < 0 else 1

        self_vel = self.vel - dv if dv else self.vel
        other_vel = other.vel - dv if dv else other.vel

        xdiff = Coord(x=self_vel.x, y=other_vel.x)
        ydiff = Coord(x=self_vel.y, y=other_vel.y)
        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = Coord(x=det(self.pos, self.pos - self_vel), y=det(other.pos, other.pos - other_vel))
        x = int(det(d, xdiff) / div)
        y = int(det(d, ydiff) / div)

        for stone in (self, other):
            stone_vel = stone.vel - dv if dv else stone.vel
            diff_x, diff_y = x - stone.pos.x, y - stone.pos.y
            if sign(diff_x) != sign(stone_vel.x) or sign(diff_y) != sign(stone_vel.y):
                return None

        return Coord(x=x, y=y)


class Hailstone3D(NamedTuple):
    pos: Coord3D
    vel: Coord3D

    @staticmethod
    def from_str(line: str) -> "Hailstone3D":
        x, y, z, dx, dy, dz = (int(x) for x in DIGITS.findall(line))
        return Hailstone3D(pos=Coord3D(x=x, y=y, z=z), vel=Coord3D(x=dx, y=dy, z=dz))

    def demote(self, dims: str = "xy") -> Hailstone2D:
        x, y = dims[0], dims[1]
        return Hailstone2D(
            pos=Coord(x=getattr(self.pos, x), y=getattr(self.pos, y)),
            vel=Coord(x=getattr(self.vel, x), y=getattr(self.vel, y)),
        )


class Storm:
    hailstones: List[Hailstone3D]
    hail_xy: List[Hailstone2D]
    hail_xz: List[Hailstone2D]
    part_one_range: range

    def __init__(self, raw_storm: str):
        self.hailstones = [Hailstone3D.from_str(x) for x in raw_storm.splitlines()]
        self.part_one_range = TEST_RANGE if len(self.hailstones) < 10 else REAL_RANGE
        self.hail_xy = [x.demote("xy") for x in self.hailstones]
        self.hail_xz = [x.demote("xz") for x in self.hailstones]

    def collisions_in_box(self) -> int:
        # Count the number of intersections that are in the correct range
        return sum(
            bool(inter := i.intersection(j)) and inter.in_range(self.part_one_range)
            for i, j in combinations(self.hail_xy, 2)
        )

    @staticmethod
    def xy_coords() -> Iterable[Coord]:
        # Spiral out from 0, 0
        yield Coord(0, 0)
        for radius in range(1, sys.maxsize):
            for y in range(-radius, radius + 1):
                yield Coord(x=radius, y=y)
                yield Coord(x=-radius, y=y)
            for x in range(-radius + 1, radius):
                yield Coord(x=x, y=radius)
                yield Coord(x=x, y=-radius)

    @staticmethod
    def z_vals() -> Iterable[int]:
        for z in range(sys.maxsize):
            yield z
            yield -z

    @staticmethod
    def check_candidate_velocity(hail: List[Hailstone2D], velocity: Coord) -> Optional[Coord]:
        all_intersections = (i.intersection(j, dv=velocity) for i, j in combinations(hail, 2))
        while (first := next(all_intersections)) is None:
            pass
        return first if all(x is None or x == first for x in all_intersections) else None

    def find_rock_origin(self) -> Coord3D:
        for rock_xy in self.xy_coords():
            xy_intersection = self.check_candidate_velocity(self.hail_xy[:10], rock_xy)
            if xy_intersection:
                for z in self.z_vals():
                    xz_intersection = self.check_candidate_velocity(self.hail_xz[:10], Coord(x=rock_xy.x, y=z))
                    if xz_intersection:
                        return Coord3D(x=xy_intersection.x, y=xy_intersection.y, z=xz_intersection.y)


def main():
    storm = Storm(read_data())
    print(f"Part one: {storm.collisions_in_box()}")
    print(f"Part two: {sum(storm.find_rock_origin())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

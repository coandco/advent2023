import time
from collections import defaultdict
from typing import Dict, List, NamedTuple, Set, Tuple

from utils import read_data


class Brick(NamedTuple):
    x: range
    y: range
    z: range

    @staticmethod
    def from_line(line: str) -> "Brick":
        raw_starts, raw_ends = line.split("~")
        starts = [int(x) for x in raw_starts.split(",")]
        ends = [int(x) for x in raw_ends.split(",")]
        return Brick(*(range(starts[i], ends[i] + 1) for i in range(3)))

    def overlap_xy(self, other: "Brick"):
        x_overlap = range(max(self.x.start, other.x.start), min(self.x.stop, other.x.stop))
        y_overlap = range(max(self.y.start, other.y.start), min(self.y.stop, other.y.stop))
        return bool(x_overlap) and bool(y_overlap)

    def overlapping_bricks(self, other_bricks: Dict["Brick", Set["Brick"]]) -> List["Brick"]:
        return sorted((x for x in other_bricks if self.overlap_xy(x)), key=lambda x: x.z.stop, reverse=True)

    def fall(self, fallen_bricks: Dict["Brick", Set["Brick"]]) -> Tuple["Brick", Set["Brick"]]:
        overlapping_bricks = self.overlapping_bricks(fallen_bricks)
        fall_distance = self.z.start - (overlapping_bricks[0].z.stop if overlapping_bricks else 1)
        fallen_brick = Brick(x=self.x, y=self.y, z=range(self.z.start - fall_distance, self.z.stop - fall_distance))
        resting_on = {x for x in overlapping_bricks if x.z.stop == overlapping_bricks[0].z.stop}
        return fallen_brick, resting_on


class Cascade:
    bricks: Dict[Brick, Set[Brick]]
    supporting: Dict[Brick, Set[Brick]]
    fallen: bool = False

    def __init__(self, raw_bricks: str):
        self.bricks = {
            x: set() for x in sorted((Brick.from_line(x) for x in raw_bricks.splitlines()), key=lambda x: x.z.start)
        }
        self.fall()
        self.supporting = defaultdict(set)
        for brick, resting_on in self.bricks.items():
            for supported in resting_on:
                self.supporting[supported].add(brick)

    def fall(self):
        new_bricks = {}
        # self.bricks should already be sorted by which ones need to fall first
        for brick in self.bricks:
            new_brick, resting_on = brick.fall(new_bricks)
            new_bricks[new_brick] = resting_on
        self.bricks = new_bricks

    def expendable_bricks(self):
        expendable_bricks = [k for k in self.bricks if not any(x == {k} for x in self.bricks.values())]
        return len(expendable_bricks)

    def get_chain(self, brick: Brick) -> int:
        eliminated_bricks = {brick}
        queue = [brick]
        while queue:
            to_zap = queue.pop()
            for supported_brick in self.supporting[to_zap]:
                if not self.bricks[supported_brick] - eliminated_bricks:
                    eliminated_bricks.add(supported_brick)
                    queue.append(supported_brick)
        return len(eliminated_bricks - {brick})


def main():
    cascade = Cascade(read_data())
    print(f"Part one: {cascade.expendable_bricks()}")
    print(f"Part two: {sum(cascade.get_chain(x) for x in cascade.bricks)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

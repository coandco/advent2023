import time
from functools import lru_cache
from typing import Tuple

from utils import read_data


class Condition:
    raw_record: str
    parity: Tuple[int]
    known_good: int
    known_bad: int

    def __init__(self, record_with_parity: str):
        self.raw_record, raw_parity = record_with_parity.split()
        self.parity = tuple(int(x) for x in raw_parity.split(","))
        self.known_good = int("".join(["1" if x == "#" else "0" for x in self.raw_record]), base=2)
        self.known_bad = int("".join(["0" if x == "." else "1" for x in self.raw_record]), base=2)

    @lru_cache(maxsize=None)
    def _count_possibilities(self, groups: Tuple[int], offset: int) -> int:
        # If we've successfully placed all the groups, this is a valid possibility
        if not groups:
            return 1
        length = len(self.raw_record) - offset
        assert sum(groups) + (len(groups) - 1) <= length, "Not enough room to fit groups!"
        group_size, other_groups = groups[0], groups[1:]
        # Each other group will take up its length, plus at least one space in between
        unavailable_space = sum(other_groups) + len(other_groups)
        available_space = length - unavailable_space
        value = 0
        for i in range(available_space - group_size + 1):
            # Make a number of 1s equal to the size of the group, then shift them i spaces from the left
            proposed_group = (pow(2, group_size) - 1) << length - (i + group_size)
            # We want to count the space after the group unless the group is at the end
            mask_size = length if not other_groups else i + group_size + 1
            mask = (pow(2, mask_size) - 1) << length - mask_size
            # Now set all known-bad and known-good bits in the proposed group to see if it matches
            real_group = ((proposed_group & self.known_bad) | self.known_good) & mask
            if proposed_group == real_group:
                value += self._count_possibilities(other_groups, offset + mask_size)
        return value

    def count_possibilities(self) -> int:
        return self._count_possibilities(groups=self.parity, offset=0)

    def unfold(self):
        self.raw_record = "?".join(self.raw_record for x in range(5))
        self.parity *= 5
        self.known_good = int("".join(["1" if x == "#" else "0" for x in self.raw_record]), base=2)
        self.known_bad = int("".join(["0" if x == "." else "1" for x in self.raw_record]), base=2)


def main():
    conditions = [Condition(x) for x in read_data().splitlines()]
    print(f"Part 1: {sum(x.count_possibilities() for x in conditions)}")
    [x.unfold() for x in conditions]
    print(f"Part 2: {sum(x.count_possibilities() for x in conditions)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

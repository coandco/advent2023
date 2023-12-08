from collections import deque
from functools import reduce
from typing import Dict, List

from utils import read_data
import time


class Map:
    map_type: str
    mapping: Dict[range, range]
    sorted_inputs: List[range]

    def __init__(self, map_type: str, mapping: Dict[range, range]):
        self.map_type = map_type
        self.mapping = mapping
        self.sorted_inputs = sorted(self.mapping.keys(), key=lambda x: x.start)

    @staticmethod
    def from_str(raw_data: str):
        lines = raw_data.splitlines()
        map_type = lines[0].split(maxsplit=1)[0]
        mapping = {}
        for line in lines[1:]:
            dest, source, length = (int(x) for x in line.split(maxsplit=2))
            source_range = range(source, source + length)
            dest_range = range(dest, dest + length)
            mapping[source_range] = dest_range
        return Map(map_type, mapping)

    def translate(self, source_num: int) -> int:
        if any(source_num in (match := x) for x in self.mapping):
            return self.mapping[match][source_num - match.start]
        return source_num

    def traverse(self, input_ranges: List[range]) -> List[range]:
        output_ranges = []
        for input_range in input_ranges:
            for my_range in self.sorted_inputs:
                before_range = range(input_range.start, min(input_range.stop, my_range.start))
                if before_range:
                    # This is part of the input range that isn't mapped, so just pass it through
                    output_ranges.append(before_range)
                overlap_range = range(max(input_range.start, my_range.start), min(input_range.stop, my_range.stop))
                if overlap_range:
                    # This part of the input range is mapped, so do the translation
                    offset = overlap_range.start - my_range.start
                    map_start = self.mapping[my_range][offset]
                    output_ranges.append(range(map_start, map_start + len(overlap_range)))
                # reduce what we're considering by what we just mapped
                input_range = range(max(input_range.start, my_range.stop), input_range.stop)
                # If we've mapped everything in this input range, move on
                if not input_range:
                    break
            # If we've gone through all of the ranges in the mapping and still have some input_range left over,
            # the remaining range just passes through
            if input_range:
                output_ranges.append(input_range)
        return output_ranges


def follow_maps(start_num: int, mappings: List[Map]) -> int:
    cur_num = start_num
    for mapping in mappings:
        cur_num = mapping.translate(cur_num)
    return cur_num


def main():
    raw = read_data().split("\n\n")
    seeds = [int(x) for x in raw[0].split(": ")[1].split()]
    mappings = [Map.from_str(x) for x in raw[1:]]
    locations = [follow_maps(x, mappings) for x in seeds]
    print(f"Part one: {min(locations)}")
    part_two_ranges = [range(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    for mapping in mappings:
        part_two_ranges = mapping.traverse(part_two_ranges)
    print(f"Part two: {min(x.start for x in part_two_ranges)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

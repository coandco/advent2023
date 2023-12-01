from typing import Dict
from utils import read_data
import time


def find_digits(line: str, mapping: Dict[str, int]):
    first = last = None
    # Find first digit
    for i in range(len(line)):
        if any(line[i:].startswith(match := x) for x in mapping.keys()):
            first = mapping[match]
            break
    # Find last digit
    for i in reversed(range(len(line))):
        if any(line[i:].startswith(match := x) for x in mapping.keys()):
            last = mapping[match]
            break

    return (first*10) + last


def main():
    lines = read_data().splitlines()
    part_one_mapping = {str(x): x for x in range(10)}
    print(f"Part one: {sum(find_digits(x, part_one_mapping) for x in lines)}")

    words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    part_two_mapping = part_one_mapping | {words[x]: x for x in range(10)}
    print(f"Part two: {sum(find_digits(x, part_two_mapping) for x in lines)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
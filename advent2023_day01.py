from typing import Dict
from utils import read_data
import time


def find_digits(line: str, mapping: Dict[str, int] = None):
    first = last = None
    # Find first digit
    for i in range(len(line)):
        # Early-out isdigit triples the performance because it's a cheaper check
        if line[i].isdigit():
            first = int(line[i])
            break
        # any stops once it hits a match, and match := x preserves which match I hit
        if any(line[i:].startswith(match := x) for x in (mapping or {}).keys()):
            first = mapping[match]
            break
    # Find last digit
    for i in reversed(range(len(line))):
        if line[i].isdigit():
            last = int(line[i])
            break
        if any(line[i:].startswith(match := x) for x in (mapping or {}).keys()):
            last = mapping[match]
            break

    return (first*10) + last


def main():
    lines = read_data().splitlines()
    print(f"Part one: {sum(find_digits(x) for x in lines)}")

    words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    word_mappings = {words[x]: x for x in range(10)}
    print(f"Part two: {sum(find_digits(x, word_mappings) for x in lines)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
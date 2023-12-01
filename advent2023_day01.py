from utils import read_data
import time


words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
mapping = {str(x): str(x) for x in range(10)} | {words[x]: str(x) for x in range(10)}
sorted_mappings = {x: {k: v for k, v in mapping.items() if len(k) == x} for x in (1, 3, 4, 5)}


def part_one(line):
    digits = [x for x in line if x.isdigit()]
    return int(f'{digits[0]}{digits[-1]}')


def part_two(line: str):
    first = last = None
    # Find first digit
    for i in range(len(line)):
        for length in sorted_mappings.keys():
            try:
                first = sorted_mappings[length][line[i:i+length]]
            except KeyError:
                pass
        if first is not None:
            break
    # Find last digit
    for i in reversed(range(len(line))):
        for length in sorted_mappings.keys():
            try:
                last = sorted_mappings[length][line[i:i+length]]
            except KeyError:
                pass
        if last is not None:
            break

    return int(f'{first}{last}')


def main():
    lines = read_data().splitlines()
    print(f"Part one: {sum(part_one(x) for x in lines)}")
    print(f"Part two: {sum(part_two(x) for x in lines)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
from utils import read_data
import time


def part_one(line):
    digits = [x for x in line if x.isdigit()]
    return int(f'{digits[0]}{digits[-1]}')


words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
mapping = {str(x): x for x in range(10)} | {words[x]: x for x in range(10)}


def part_two(line: str):
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
    print(f"Part one: {sum(part_one(x) for x in lines)}")
    print(f"Part two: {sum(part_two(x) for x in lines)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
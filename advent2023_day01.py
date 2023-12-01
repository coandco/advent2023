from utils import read_data
import time
import re


def part_one(line):
    digits = [x for x in line if x.isdigit()]
    return int(f'{digits[0]}{digits[-1]}')


mapping = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine'
}
reversed_mapping = {v: k for k, v in mapping.items()}
DIGIT_WORDS = re.compile('(?=(' + "|".join(mapping.values()) + '))')


def part_two(line: str):
    for num, word in mapping.items():
        line = line.replace(num, word)
    digits = [reversed_mapping[x] for x in DIGIT_WORDS.findall(line)]
    return int(f'{digits[0]}{digits[-1]}')


def main():
    lines = read_data().splitlines()
    print(f"Part one: {sum(part_one(x) for x in lines)}")
    print(f"Part two: {sum(part_two(x) for x in lines)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
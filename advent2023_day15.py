import time
from typing import Dict

from utils import read_data


def lhash(tohash: str) -> int:
    curval = 0
    for char in tohash:
        curval += ord(char)
        curval *= 17
        curval %= 256
    return curval


def score_one(boxnum: int, box: Dict[str, int]) -> int:
    return boxnum * sum(i * v for i, v in enumerate(box.values(), start=1))


def main():
    instructions = read_data().split(",")
    print(f"Part one: {sum(lhash(x) for x in instructions)}")
    boxes = [{} for _ in range(256)]
    for instruction in instructions:
        if instruction.endswith("-"):
            boxes[lhash(instruction[:-1])].pop(instruction[:-1], None)
        else:
            label, value = instruction.split("=")
            boxes[lhash(label)][label] = int(value)
    print(f"Part two: {sum(score_one(i, x) for i, x in enumerate(boxes, start=1))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

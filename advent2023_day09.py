from typing import List

from utils import read_data
import time


class Sequence:
    sequence: List[int]

    def __init__(self, line: str):
        self.sequence = [int(x) for x in line.split()]

    def predict(self, reversed=False):
        derivatives = [self.sequence[::-1]] if reversed else [self.sequence]
        while not all(x == 0 for x in derivatives[-1]):
            current = derivatives[-1]
            derivatives.append([current[i+1] - current[i] for i in range(len(current) - 1)])
        previous = derivatives.pop()
        while derivatives:
            current = derivatives[-1]
            current.append(current[-1] + previous[-1])
            previous = derivatives.pop()
        return previous[-1]


def main():
    sequences = [Sequence(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(x.predict() for x in sequences)}")
    print(f"Part two: {sum(x.predict(reversed=True) for x in sequences)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

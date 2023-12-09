from collections import deque
from typing import List

from utils import read_data
import time


class Sequence:
    sequence: List[int]

    def __init__(self, line: str):
        self.sequence = [int(x) for x in line.split()]

    def predict(self, time_travel=False):
        derivatives = [deque(self.sequence)]
        while not all(x == 0 for x in derivatives[-1]):
            current = derivatives[-1]
            derivative = deque(current[i+1] - current[i] for i in range(len(current) - 1))
            derivatives.append(derivative)
        previous = derivatives.pop()
        while derivatives:
            current = derivatives[-1]
            if time_travel:
                current.appendleft(current[0] - previous[0])
            else:
                current.append(current[-1] + previous[-1])
            previous = derivatives.pop()
        return previous[0] if time_travel else previous[-1]


def main():
    sequences = [Sequence(x) for x in read_data().splitlines()]
    predictions = [x.predict() for x in sequences]
    print(f"Part one: {sum(predictions)}")
    backwards_predictions = [x.predict(time_travel=True) for x in sequences]
    print(f"Part two: {sum(backwards_predictions)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

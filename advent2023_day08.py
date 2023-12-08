from math import lcm
from typing import Dict, Tuple, Iterable

from utils import read_data
import time
import re

NAMES = re.compile(r'[0-9A-Z]+')


class Network:
    instructions: str
    nodes: Dict[str, Tuple[str, str]]

    def __init__(self, raw_str: str):
        lines = raw_str.splitlines()
        self.instructions = lines[0]
        self.nodes = {}
        for line in lines[2:]:
            node, left, right = NAMES.findall(line)
            self.nodes[node] = (left, right)

    def instruction_loop(self) -> Iterable[int]:
        while True:
            for char in self.instructions:
                yield 1 if char == 'R' else 0

    def traverse(self) -> int:
        cur_node = 'AAA'
        steps = 0
        for dir in self.instruction_loop():
            if cur_node == 'ZZZ':
                break
            cur_node = self.nodes[cur_node][dir]
            steps += 1
        return steps

    def find_period(self, node: str) -> int:
        steps = 0
        for dir in self.instruction_loop():
            node = self.nodes[node][dir]
            steps += 1
            if node.endswith('Z'):
                return steps

    def traverse_part_two(self) -> int:
        nodes = [x for x in self.nodes if x.endswith('A')]
        periods = [self.find_period(x) for x in nodes]
        return lcm(*periods)


def main():
    network = Network(read_data())
    print(f"Part one: {network.traverse()}")
    print(f"Part two: {network.traverse_part_two()}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

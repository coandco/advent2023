from collections import defaultdict
from typing import Dict, Set

from utils import read_data
import time
import re

LETTERS = re.compile(r'[a-z]+')


class Components:
    connections: Dict[str, Set[str]]
    in_group: Set[str]

    def __init__(self, raw_connections: str):
        self.connections = defaultdict(set)
        for line in raw_connections.splitlines():
            key, *values = LETTERS.findall(line)
            self.connections[key] |= set(values)
            for value in values:
                self.connections[value].add(key)
        self.in_group = set(self.connections)
        self.split()

    def external_connections(self, node: str):
        return len(self.connections[node] - self.in_group)

    def split(self):
        while sum(self.external_connections(x) for x in self.in_group) != 3:
            most_connected_node = max(self.in_group, key=self.external_connections)
            self.in_group.remove(most_connected_node)


def main():
    components = Components(read_data())
    print(f"Part one: {len(components.in_group) * (len(components.connections) - len(components.in_group))}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

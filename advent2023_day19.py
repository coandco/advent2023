import re
import time
from collections import deque
from math import prod
from typing import Dict, List, NamedTuple, Optional, Tuple

from utils import read_data

DIGITS = re.compile(r"\d+")
ATTRS = "xmas"
ATTR_INDICES = {x: i for i, x in enumerate(ATTRS)}


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def from_str(raw_part: str) -> "Part":
        return Part(*(int(x) for x in DIGITS.findall(raw_part)))

    def value(self):
        return sum(self)


class PartRange(NamedTuple):
    x: range
    m: range
    a: range
    s: range

    @staticmethod
    def full_range() -> "PartRange":
        return PartRange(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))

    def combinations(self) -> int:
        return prod(len(x) for x in self)

    def update_attr(self, attr_num: int, new_range: range) -> "PartRange":
        mutable = list(self)
        mutable[attr_num] = new_range
        return PartRange(*mutable)


class Rule(NamedTuple):
    attr: int
    op: str
    val: int

    @staticmethod
    def from_str(raw: str):
        return Rule(ATTR_INDICES[raw[0]], raw[1], int(raw[2:]))

    def matches(self, part: Part) -> bool:
        return part[self.attr] > self.val if self.op == ">" else part[self.attr] < self.val

    def split_range(self, part_range: PartRange) -> Tuple[PartRange, Optional[PartRange]]:
        if self.val in (rating := part_range[self.attr]):
            if self.op == ">":
                original, new = range(rating.start, self.val + 1), range(self.val + 1, rating.stop)
            else:
                new, original = range(rating.start, self.val), range(self.val, rating.stop)
            return part_range.update_attr(self.attr, original), part_range.update_attr(self.attr, new)
        return part_range, None


class Workflow:
    name: str
    rules: Dict[Rule, str]
    default: str

    def __init__(self, line: str):
        self.rules = {}
        # Strip off the final }
        self.name, raw_rules = line[:-1].split("{", maxsplit=1)
        *raw_rule_list, self.default = raw_rules.split(",")
        for raw_rule in raw_rule_list:
            rulestr, dest = raw_rule.split(":")
            self.rules[Rule.from_str(rulestr)] = dest

    def get_dest(self, part: Part) -> str:
        return self.rules[matched] if any((matched := x).matches(part) for x in self.rules) else self.default

    def split_range(self, to_split: PartRange) -> Tuple[List[Tuple[PartRange, str]], List[PartRange]]:
        accepted_ranges = []
        new_map = []
        for rule, dest in self.rules.items():
            to_split, new_range = rule.split_range(to_split)
            if new_range:
                if dest == "A":
                    accepted_ranges.append(new_range)
                elif dest == "R":
                    pass
                else:
                    new_map.append((new_range, dest))
        if self.default == "A":
            accepted_ranges.append(to_split)
        elif self.default == "R":
            pass
        else:
            new_map.append((to_split, self.default))
        return new_map, accepted_ranges


class System:
    workflows: Dict[str, Workflow]

    def __init__(self, raw_workflows: str):
        self.workflows = {(r := Workflow(x)).name: r for x in raw_workflows.splitlines()}

    def is_accepted(self, part: Part) -> bool:
        cur_workflow = "in"
        while cur_workflow not in ("A", "R"):
            cur_workflow = self.workflows[cur_workflow].get_dest(part)
        return cur_workflow == "A"

    def all_accepted(self) -> int:
        ranges = deque()
        ranges.append((PartRange.full_range(), "in"))
        accepted_ranges = []
        while ranges:
            cur_range, dest = ranges.popleft()
            new_ranges, new_accepted = self.workflows[dest].split_range(cur_range)
            ranges.extend(new_ranges)
            accepted_ranges.extend(new_accepted)
        return sum(x.combinations() for x in accepted_ranges)


def main():
    raw_workflows, raw_parts = read_data().split("\n\n")
    system = System(raw_workflows)
    parts = [Part.from_str(x) for x in raw_parts.splitlines()]
    print(f"Part one: {sum(x.value() for x in parts if system.is_accepted(x))}")
    print(f"Part two: {system.all_accepted()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

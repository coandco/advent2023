from typing import NamedTuple, Dict

from utils import read_data
import time
import re

DIGITS = re.compile(r'\d+')


ATTRS = "xmas"
ATTR_INDICES = {x: i for i, x in enumerate(ATTRS)}


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def from_str(raw_part: str) -> 'Part':
        return Part(*(int(x) for x in DIGITS.findall(raw_part)))

    def value(self):
        return sum(self)


class Rule(NamedTuple):
    attr: int
    op: str
    val: int

    @staticmethod
    def from_str(raw: str):
        return Rule(ATTR_INDICES[raw[0]], raw[1], int(raw[2:]))

    def matches(self, part: Part) -> bool:
        return part[self.attr] > self.val if self.op == '>' else part[self.attr] < self.val

    def __repr__(self):
        return f"Rule({ATTRS[self.attr]}, {self.op}, {self.val})"


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


class System:
    workflows: Dict[str, Workflow]

    def __init__(self, raw_workflows: str):
        self.workflows = {(r := Workflow(x)).name: r for x in raw_workflows.splitlines()}

    def is_accepted(self, part: Part) -> bool:
        cur_workflow = "in"
        while cur_workflow not in ("A", "R"):
            cur_workflow = self.workflows[cur_workflow].get_dest(part)
        return cur_workflow == 'A'


def main():
    TEST = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    raw_workflows, raw_parts = read_data().split("\n\n")
    system = System(raw_workflows)
    parts = [Part.from_str(x) for x in raw_parts.splitlines()]
    accepted = [x for x in parts if system.is_accepted(x)]
    print(f"Part one: {sum(x.value() for x in accepted)}")



if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

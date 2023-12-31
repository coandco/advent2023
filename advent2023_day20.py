import time
from collections import deque
from math import lcm, prod
from typing import Dict, List, Optional, Tuple, Union

from utils import read_data


class Module:
    name: str
    outputs: List[str]

    def __init__(self, line: str):
        self.name, raw_outputs = line.split(" -> ")
        self.outputs = raw_outputs.split(", ")

    @staticmethod
    def from_str(line: str) -> Union["Module", "FlipFlopModule", "ConjunctionModule"]:
        if line[0] == "%":
            return FlipFlopModule(line[1:])
        elif line[0] == "&":
            return ConjunctionModule(line[1:])
        else:
            return Module(line)

    def handle_pulse(self, pulse_from: str, val: int) -> Optional[int]:
        return val


class FlipFlopModule(Module):
    state: bool = False

    def handle_pulse(self, pulse_from: str, val: bool) -> Optional[bool]:
        if val:
            return None
        self.state = not self.state
        return self.state


class ConjunctionModule(Module):
    inputs: Dict[str, bool]

    def set_inputs(self, inputs: List[str]):
        self.inputs = {x: False for x in inputs}

    def handle_pulse(self, pulse_from: str, val: bool) -> Optional[bool]:
        self.inputs[pulse_from] = val
        return not all(self.inputs.values())


class Machine:
    modules: Dict[str, Union[Module, FlipFlopModule, ConjunctionModule]]
    rx_input: str
    times_pushed: int = 0
    input_cycles: Dict[str, int]

    def __init__(self, raw_modules: str):
        self.modules = {(m := Module.from_str(x)).name: m for x in raw_modules.splitlines()}
        for name, module in self.modules.items():
            if isinstance(module, ConjunctionModule):
                module.set_inputs([x for x in self.modules if name in self.modules[x].outputs])
        self.rx_input = next(x for x in self.modules if "rx" in self.modules[x].outputs)
        self.input_cycles = {x: 0 for x in self.modules[self.rx_input].inputs}

    def _push_button(self) -> Tuple[int, int]:
        pulses = deque([("button", "broadcaster", False)])
        counts = [1, 0]  # one low signal sent and no high signals
        self.times_pushed += 1
        while pulses:
            source, dest, val = pulses.popleft()
            # If it's a high pulse coming from one of our upstream inputs and we haven't already found its cycle
            if val and self.input_cycles.get(source, None) == 0:
                self.input_cycles[source] = self.times_pushed
            new_pulse_val = self.modules[dest].handle_pulse(source, val)
            if new_pulse_val is not None:
                counts[new_pulse_val] += len(self.modules[dest].outputs)
                pulses.extend((dest, x, new_pulse_val) for x in self.modules[dest].outputs if x in self.modules)
        # return low_count, high_count
        return counts[0], counts[1]

    def push_button(self, times: int) -> Tuple[int, int]:
        total_low, total_high = 0, 0
        for _ in range(times):
            low, high = self._push_button()
            total_low, total_high = total_low + low, total_high + high
        return total_low, total_high

    def activate_rx(self) -> int:
        while not all(self.input_cycles.values()):
            self._push_button()
        return lcm(*self.input_cycles.values())


def main():
    machine = Machine(read_data())
    print(f"Part one: {prod(machine.push_button(1000))}")
    machine = Machine(read_data())
    print(f"Part two: {machine.activate_rx()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

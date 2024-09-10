from collections import defaultdict
from enum import Enum, auto
from pathlib import Path

# flip-flop % : on/off, default off. receives low: on -> off, sends
ex1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

ex2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


class Pulse(Enum):
    low = auto()
    high = auto()


class State(Enum):
    on = auto()
    off = auto()


class Module:

    def __init__(self, name: str, dest: list[str]):
        self.name = name
        self.dest = dest
        self.last_received: Pulse = None

    def send(self, src: str, pulse: Pulse) -> None | Pulse:
        self.last_received = pulse
        return None


class FlipFlopModule(Module):

    def __init__(self, name: str, dest: list[str]):
        super().__init__(name, dest)
        self.state = State.off

    def send(self, src: str, pulse: Pulse) -> None | Pulse:
        super().send(src, pulse)
        if pulse is Pulse.high:
            return None

        if self.state is State.on:
            self.state = State.off
            return Pulse.low

        self.state = State.on
        return Pulse.high

    def __repr__(self):
        return f'{self.__class__.__name__}({self.state})'


class ConjunctionModule(Module):

    def __init__(self, name: str, dest: list[str]):
        super().__init__(name, dest)
        self.src: dict[str, Pulse] = {}

    def send(self, src: str, pulse: Pulse) -> None | Pulse:
        super().send(src, pulse)
        # update memory
        self.src[src] = pulse

        if all(p is Pulse.high for p in self.src.values()):
            return Pulse.low

        return Pulse.high

    def __repr__(self):
        return f'{self.__class__.__name__}({self.src})'


class BroadcastModule(Module):

    def __init__(self, dest: list[str]):
        super().__init__('broadcaster', dest)

    def send(self, src: str, pulse: Pulse) -> None | Pulse:
        super().send(src, pulse)
        return Pulse.low


def parse_data(data: str):
    modules = {}
    for line in data.splitlines():
        mod_desc, dest = line.split(' -> ')
        dest = dest.split(', ')

        if mod_desc == 'broadcaster':
            modules['broadcaster'] = BroadcastModule(dest)
            continue

        name = mod_desc[1:]
        cls = FlipFlopModule if mod_desc[0] == '%' else ConjunctionModule
        modules[name] = cls(name, dest)

    # make conjunction modules aware of their sources
    conj = {
        name: module
        for name, module in modules.items()
        if isinstance(module, ConjunctionModule)
    }
    for m in modules.values():
        for dname in m.dest:
            if dname not in conj:
                continue

            dmod = modules[dname]
            # dmod is a conjunction module whose source is m
            dmod.src[m.name] = Pulse.low

    # check for undefined modules
    untyped = []
    for m in modules.values():
        for d in m.dest:
            if d not in modules:
                untyped.append(d)
    for name in untyped:
        modules[name] = Module(name, [])

    return modules

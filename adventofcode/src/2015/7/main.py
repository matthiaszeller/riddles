import operator
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

import networkx as nx

from utils import *


class GateType(Enum):
    OR = 'OR'
    LSHIFT = 'LSHIFT'
    RSHIFT = 'RSHIFT'
    AND = 'AND'
    NOT = 'NOT'
    ID = 'ID'
    ASSIGN = 'ASSIGN'


class AbstractInt:

    NBITS: int = None

    def __init__(self, bits: str):
        assert len(bits) <= self.NBITS
        self.bits = bits.zfill(self.NBITS)

    def _bitwise_binop(self, op, other: 'AbstractInt'):
        bit_string = (op(int(b1), int(b2)) for b1, b2 in zip(self.bits, other.bits))
        bit_string = map(str, bit_string)
        return self.__class__(''.join(bit_string))

    def _bitwise_op(self, op):
        bit_string = (op(int(b)) for b in self.bits)
        bit_string = map(str, bit_string)
        return self.__class__(''.join(bit_string))

    def __and__(self, other):
        return self._bitwise_binop(operator.and_, other)

    def __or__(self, other):
        return self._bitwise_binop(operator.or_, other)

    def __invert__(self):
        return self._bitwise_op(lambda b: int(not b))

    def __lshift__(self, n):
        n = int(n)
        return self.__class__(self.bits[n:] + '0' * n)

    def __rshift__(self, n):
        n = int(n)
        return self.__class__(self.bits[:-n])


    @classmethod
    def from_int(cls, value: int | str):
        return cls(bin(int(value))[2:])

    def __int__(self):
        return int(self.bits, 2)

    def __repr__(self):
        return f'{self.__class__.__name__}({int(self)})'


class Int16(AbstractInt):

    NBITS = 16


def compute_gate(type: GateType, args: list[Int16 | int, ...]):
    match type:
        case GateType.ID:
            return args[0]
        case GateType.ASSIGN:
            return args[0]
        case GateType.NOT:
            return ~ args[0]
        case GateType.AND:
            return args[0] & args[1]
        case GateType.OR:
            return args[0] | args[1]
        case GateType.LSHIFT:
            return args[0] << args[1]
        case GateType.RSHIFT:
            return args[0] >> args[1]


@dataclass(frozen=True)
class Gate:
    type: GateType | str
    args: tuple[str | int | Int16, ...]

    @property
    def input_variables(self) -> tuple[str, ...]:
        return tuple(a for a in self.args if isinstance(a, str))


@dataclass(frozen=True)
class Instruction:
    inp: Gate
    out: str


def parse_program(prog: str):
    def is_number(n: str):
        return n.lstrip('-').isdigit()

    ins = []
    for line in prog.splitlines():
        left, dst = line.split(' -> ')

        gate = tuple(left.split())

        if len(gate) == 1:
            if is_number(gate[0]):
                ins.append(
                    Instruction(
                        Gate(GateType.ASSIGN, (Int16.from_int(gate[0]), )),
                        dst
                    )
                )
            else:
                ins.append(Instruction(
                    Gate(GateType.ID, gate),
                    dst
                ))
        elif len(gate) == 2:
            ins.append(Instruction(Gate(GateType.NOT, gate[1:]), dst))
        else:
            v1, op, v2 = gate
            if is_number(v2):
                v2 = Int16.from_int(v2)
            elif is_number(v1):
                v1, v2 = v2, Int16.from_int(v1)

            ins.append(Instruction(
                Gate(GateType(op), (v1, v2)),
                dst
            ))

    return ins


def topological_sort(ins: list[Instruction]) -> list[Instruction]:
    G = nx.DiGraph()

    input_map = defaultdict(set)
    for i in ins:
        for a in i.inp.input_variables:
            input_map[a].add(i)

    for u in ins:
        for v in input_map[u.out]:
            G.add_edge(u, v)

    out = list(nx.topological_sort(G))
    return out


def run_program(ins: list[Instruction]):
    ins = topological_sort(ins)
    record: dict[str, int] = {}

    for i in ins:
        input = tuple(record.get(v, v) for v in i.inp.args)
        record[i.out] = compute_gate(i.inp.type, input)

    return record


ins = parse_program(load_data())
out = run_program(ins)
print('wire a value:', out['a'])

# part 2: simply add new instruction
new_ins = f"{int(out['a'])} -> b"
ins.extend(parse_program(new_ins))
print('added instruction', new_ins)
out = run_program(ins)
print('wire a value:', out['a'])

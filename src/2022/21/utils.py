import operator
from pathlib import Path
from typing import Callable

OPERATOR_MAP = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str, map_op: bool = True):
    src: dict[str, int] = {}
    wait: dict[str, tuple[Callable, str, str]] = {}
    for line in data.splitlines():
        id, rest = line.split(': ')
        try:
            n = int(rest)
            src[id] = n
        except ValueError:
            a, op, b = rest.split()
            if map_op:
                op = OPERATOR_MAP[op]
            wait[id] = (op, a, b)

    return src, wait


example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
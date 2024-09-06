

from utils import *


def is_contained(a: tuple[int, int], b: tuple[int, int]):
    (a1, a2), (b1, b2) = sorted((a, b))
    return b2 <= a2 or a1 == b1


def solve(data: list[tuple[int]]):
    return sum(is_contained(tpl[:2], tpl[2:]) for tpl in data)


data = parse_data(load_data())

for tpl in data:
    print(f'{is_contained(tpl[:2], tpl[2:]):<5} {tpl}')

print(solve(data))

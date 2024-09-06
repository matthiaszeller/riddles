

from utils import *


def overlaps(a: tuple[int, int], b: tuple[int, int]):
    (a1, a2), (b1, b2) = sorted((a, b))
    return b1 <= a2


data = parse_data(load_data())

n = 0
for tpl in data:
    o = overlaps(tpl[:2], tpl[2:])
    n += o
    print(f'{o:<3} {tpl}')

print(n)

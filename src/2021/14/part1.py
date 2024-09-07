from collections import Counter

from utils import *

# Straightforward implementation


def step(template: str, rules: dict[str, str]):
    polymer = ''
    for a, b in zip(template[:-1], template[1:]):
        polymer += a + rules[a + b]

    polymer += template[-1]
    return polymer


def solve(template: str, rules: dict[str, str], n: int = 10):
    for _ in range(n):
        template = step(template, rules)

    counts = Counter(template)
    (_, c1), *_, (_, c2) = counts.most_common()
    return c1 - c2


data = parse_data(load_data())
n = solve(*data)
print(n)


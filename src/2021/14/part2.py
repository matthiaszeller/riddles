from collections import Counter

from utils import *


# 40 steps leads to combinatorial explosion... cannot possibly simulate it
# Idea: try to map each original rule to a dictionary of counts
# we do not care about the sequence of all letters, just about the number of pairs

# at each step, we can easily calculate the number of pairs after the step
# in the end, we must count the standalone letters, but they're duplicated:
#
# for instance, starting with CHN (using example rules),
# step 0: CHN       pairs CH (1), HN (1)
# step 1: CBHCN     pairs CB (1), BH (1), HC (1), CN (1)
#                   letter counts: C (3), B(2), H(2), N(1)
#
# Each letter that is inserted will be counted twice: XZ -> XYZ will have pairs XY, YZ
# so simply maintain counts of duplicated letters and subtract in the end
#
# Note: must not forget the duplicate letters due to initial pair generation: all letters in the middle of the template


def mult_counter(c: Counter, n: int):
    return {k: n * v for k, v in c.items()}


def transform_rules(rules: dict[str, str]) -> dict[str, tuple[Counter, Counter]]:
    out = {}
    for pair, inserted in rules.items():
        p1 = pair[0] + inserted
        p2 = inserted + pair[1]
        out[pair] = Counter((p1, p2)), Counter((inserted,))

    return out


def step(counts: Counter[str], duplicates: Counter[str], rules: dict[str, tuple[Counter, Counter]]):
    out = Counter()
    duplicates = duplicates.copy()
    for pair, n in counts.items():
        new_pairs, new_duplicates = rules[pair]
        out += mult_counter(new_pairs, n)
        duplicates += mult_counter(new_duplicates, n)

    return out, duplicates


def template2counts(template: str):
    pair_counts = Counter(a + b for a, b in zip(template[:-1], template[1:]))
    duplicates = Counter(template[1:-1])
    return pair_counts, duplicates


def solve(template: str, rules: dict[str, str], n: int):
    rules = transform_rules(rules)
    counts, duplicates = template2counts(template)
    for _ in range(n):
        counts, duplicates = step(counts, duplicates, rules)

    return counts, duplicates


def compute_solution(pair_counts: Counter, dupl: Counter):
    letter_counts = Counter()
    for pair, n in pair_counts.items():
        letter_counts[pair[0]] += n
        letter_counts[pair[1]] += n

    for letter, n in dupl.items():
        letter_counts[letter] -= n

    (_, c1), *_, (_, c2) = letter_counts.most_common()
    return c1 - c2, letter_counts


template, rules = parse_data(load_data())
counts, dupl = solve(template, rules, 40)
n, lcounts = compute_solution(counts, dupl)


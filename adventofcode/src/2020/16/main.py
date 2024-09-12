
# Standard library imports
import pathlib
import sys
from collections import defaultdict, Counter
from typing import TypeVar

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from adventofcode.src.utils import (
    # --- I/O ---
    load_riddle_files, line_parser, parse_nums, parse_grid, print_grid, capture_stdout, print_formatted,
    # --- Other ---
    memoize, chunkify, all_unique,
    # --- Math ---
    factors, gcd, lcm, primes,
    # --- Hashing ---
    md5, sha256, knot_hash, HEX_DIRS, hex_distance,
    # --- Point helper classes ---
    PointND, Point2D, Point3D, DIRS_4, DIRS_8,
    # --- Bitwise operations ---
    UInt8, UInt16, UInt32, UInt64,
)


# @line_parser
def parse_data(input: str):
    """Parse input."""
    def f(line):
        field, rng = line.split(': ')
        return field, parse_nums(rng.replace('-', ' '))

    fields, my, others = input.split('\n\n')
    my = parse_nums(my)
    others = list(map(parse_nums, others.splitlines()[1:]))
    fields = list(map(f, fields.splitlines()))
    return fields, my, others


def part1(data):
    """Solve part 1."""
    fields, my, others = data
    valid_values = set()
    for _, (a, b, c, d) in fields:
        valid_values.update(range(a, b+1))
        valid_values.update(range(c, d+1))

    N = 0
    valid = []
    for i, o in enumerate(others):
        ok = True
        for n in o:
            if n not in valid_values:
                N += n
                print(n)
                ok = False

        if ok:
            valid.append(i)

    return N, valid


def part2(data):
    """Solve part 2."""
    _, valid = part1(data)
    fields, my, others = data
    others = np.array([others[i] for i in valid])

    match = defaultdict(set)
    for f, (a, b, c, d) in fields:
        for i, other_vals in enumerate(others.T):
            ok = (a <= other_vals) & (other_vals <= b)
            ok |= (c <= other_vals) & (other_vals <= d)
            if ok.all():
                match[f].add(i)

    assign = {}
    while match:
        rmnum = set()
        rmfield = set()
        for f, s in match.items():
            if len(s) == 1:
                i = s.pop()
                assign[f] = i
                rmfield.add(f)
                rmnum.add(i)

        for f in rmfield:
            del match[f]
        for s in match.values():
            s.difference_update(rmnum)

    departures = [
        my[i] for i in [
            j for f, j in assign.items() if 'departure' in f
        ]
    ]

    return np.prod(departures)


if __name__ == '__main__':
    examples, data = load_riddle_files(__file__)
    for i, example in enumerate(examples):
        print_formatted(f'{"=" * 20} Example {i + 1}:', color='g', bold=True)
        print(example)
        example = parse_data(example)
        print_formatted(f'{"-" * 20} Parsed', color='b')
        print(example)
        print_formatted(f'{"-" * 20} Solution', color='b')
        print_formatted(f'Part 1: {part1(example)}', color='r')
        print_formatted(f'Part 2: {part2(example)}', color='r')
        print()

    # sys.exit()
    data = parse_data(data)
    print_formatted(f'{"=" * 20} Data:', color='g', bold=True)
    out1, res1 = capture_stdout(part1, data, discard=False)
    print_formatted(f'Part 1: {res1}', color='r', bold=True)
    out2, res2 = capture_stdout(part2, data, discard=False)
    print_formatted(f'Part 2: {res2}', color='r', bold=True)

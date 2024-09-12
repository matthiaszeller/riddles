import operator
# Standard library imports
import pathlib
import re
import sys
from functools import reduce
from typing import TypeVar

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


@line_parser
def parse_data(input: str):
    """Parse input."""
    return input


def part1_line(data):
    """Solve part 1."""
    def parse_term(t):
        t = t.split()
        n = int(t[0])
        op = None
        for e in t[1:]:
            if e == '*':
                op = operator.mul
            elif e == '+':
                op = operator.add
            else:
                n = op(n, int(e))

        return str(n)

    expr = data
    # use regex to parse innermost parentheses
    while res := re.findall(r'\([^\(\)]+\)', expr):
        print('.')
        for termp in res:
            term = termp.strip('()')
            expr = expr.replace(termp, parse_term(term))

    expr = parse_term(expr)

    return int(expr)


def part1(data):
    return sum(map(part1_line, data))


def part2_line(line):
    """Solve part 2."""
    def parse_term(t):
        def parse_add(t):
            try:
                return eval(t)
            except:
                pass

        t = t.split('*')
        t = list(map(parse_add, t))
        return str(reduce(operator.mul, t))

    expr = line
    # use regex to parse innermost parentheses
    while res := re.findall(r'\([^\(\)]+\)', expr):
        print('.')
        for termp in res:
            term = termp.strip('()')
            expr = expr.replace(termp, parse_term(term))

    expr = parse_term(expr)

    return int(expr)


def part2(data):
    return sum(map(part2_line, data))


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

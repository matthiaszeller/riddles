
# Standard library imports
import pathlib
import sys
from collections import defaultdict
from itertools import product
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
    UInt8, UInt64, UInt32, UInt64,
)

DataType = TypeVar('DataType')


@line_parser
def parse_data(input: str) -> DataType:
    """Parse input."""
    if input.startswith('mask'):
        return input.split(' = ')[1]

    return parse_nums(input, False)


def parse_mask(mask: str):
    m1 = UInt64(mask.replace('X', '0'))
    m0 = UInt64(mask.replace('1', 'X').replace('0', '1').replace('X', '0'))
    mx = UInt64(mask.replace('1', '0').replace('X', '1'))
    return m1, m0, mx


def part1(data: DataType):
    """Solve part 1."""
    mem = {}
    m1, m0 = None, None
    for item in data:
        if isinstance(item, str):
            m1, m0, _ = parse_mask(item)
            print(m1.bits)
            print(m0.bits)
            continue

        addr, val = item
        v = UInt64(val)
        v = (v | m1) & ~m0
        print('val', val)
        print(UInt64(val).bits)
        print(v.bits)
        v = int(v)
        print('writing', v, 'to addr', addr)
        mem[addr] = v

    return sum(mem.values())


def mask_factory(mask: str):
    mask = mask.zfill(64)
    m1, *_ = parse_mask(mask)
    ids = [i for i, b in enumerate(mask) if b == 'X']

    def addr_iter(val: int):
        val = UInt64(val) | m1
        bits = list(val.bits)
        for i in ids:
            bits[i] = '{}'

        bits = ''.join(bits)
        for comb in product('01', repeat=len(ids)):
            addr = bits.format(*comb)
            yield int(UInt64(addr))

    return addr_iter


def part2(data: DataType):
    """Solve part 2."""
    mem = {}
    for item in data:
        if isinstance(item, str):
            print('new mask')
            print(item)
            addr_iter = mask_factory(item)
            continue

        addr, val = item
        for a in addr_iter(addr):
            print('addr', a, 'val', val)
            mem[a] = val

    return sum(mem.values())


if __name__ == '__main__':
    examples, data = load_riddle_files(__file__)
    for i, example in enumerate(examples[1:]):
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

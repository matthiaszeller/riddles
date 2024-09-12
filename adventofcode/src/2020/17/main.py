
# Standard library imports
import pathlib
import sys
from typing import TypeVar

import numpy as np
from scipy.signal import convolve

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from adventofcode.src.utils import (
    # --- I/O ---
    load_riddle_files, line_parser, parse_nums, parse_grid, print_grid as print_grid_, capture_stdout, print_formatted,
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
    return parse_grid(input)


MASK = np.ones((3, 3, 3), int)
MASK[1, 1, 1] = 0


def print_grid(grid):
    m = (grid == '#').any((1,2))
    for i, sub in enumerate(grid[m]):
        print('--- z =', i)
        print_grid_(sub)


def step(grid, mask=MASK):
    grid = grid.copy()
    mask_on = grid == '#'
    pad = any(mask_on.take(i, axis=axis).any() for axis in range(grid.ndim) for i in (0, -1))
    if pad:
        grid = np.pad(grid, 1, constant_values='.')
        mask_on = grid == '#'

    mask_off = grid == '.'

    nactive = convolve(mask_on, mask, 'same')
    rule1 = ~((nactive == 2) | (nactive == 3))
    grid[mask_on & rule1] = '.'

    rule2 = nactive == 3
    grid[mask_off & rule2] = '#'
    return grid


def part1(data):
    """Solve part 1."""
    grid = data.reshape((1,) + data.shape)
    #grid = np.pad(grid, ((1, 1), (0, 0), (0, 0)), constant_values='.')
    print_grid(grid)
    print('-' * 10)
    for _ in range(6):
        grid = step(grid)
        print_grid(grid)
        print('-' * 10)

    return (grid == '#').sum()


MASK4D = np.ones((3,3,3,3), int)
MASK4D[1, 1, 1, 1] = 0


def part2(data):
    """Solve part 2."""
    grid = data.reshape((1, 1) + data.shape)
    for _ in range(6):
        grid = step(grid, mask=MASK4D)

    return (grid == '#').sum()


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

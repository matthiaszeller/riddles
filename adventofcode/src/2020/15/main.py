
# Standard library imports
import pathlib
import sys
from collections import Counter, defaultdict
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


# @line_parser
def parse_data(input: str):
    """Parse input."""
    return parse_nums(input)


def part1(data, N=2020):
    """Solve part 1."""
    def do_speak_num(n: int, i: int):
        e = spoken_nums[n]
        if len(e) == 0:
            e = (i, )
        elif len(e) == 1:
            e += (i, )
        else:
            e = (e[1], i)

        spoken_nums[n]= e

    spoken_nums = defaultdict(tuple)
    for i, n in enumerate(data):
        do_speak_num(n, i)

    last_num = data[-1]
    print('initial state', spoken_nums, 'last spoken', last_num)
    for i in range(len(data), N):
        last_spoken = spoken_nums[last_num]

        if len(last_spoken) == 1:
            last_num = 0
        else:
            j, k = last_spoken
            age = k - j
            last_num = age

        do_speak_num(last_num, i)
        #print('round', i, 'speak num', last_num, 'state', spoken_nums)

    return last_num


def part2(data):
    """Solve part 2."""
    return part1(data, N=30000000)


if __name__ == '__main__':
    examples, data = load_riddle_files(__file__)
    for i, example in enumerate(examples[:0]):
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

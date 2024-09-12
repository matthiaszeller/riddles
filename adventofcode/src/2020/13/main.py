
# Standard library imports
import pathlib
import sys
from typing import TypeVar

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))


# Part 1: easy
# Part 2: modulo arithmetics, super hard for me. I had to lookup into extended gcd/Euclidean algorithm,
#         diophantine equations, and then combining all solutions using Chinese remainder theorem.


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

DataType = TypeVar('DataType')


# @line_parser
def parse_data(input: str) -> DataType:
    """Parse input."""
    l1, l2 = input.splitlines()
    E = int(l1)
    ids = np.array(l2.split(','))
    ids[ids == 'x'] = '-1'
    return E, ids.astype(int)


def part1(data: DataType):
    """Solve part 1."""
    E, ids = data
    ids = ids[ids >= 0]
    nwait = E // ids
    exact = (nwait * ids) % E == 0

    if exact.any():
        (i, ), = exact.where()
        print('bus', i, 'id', ids[i], 'waits 0 min, after', nwait[i], 'rounds')

    wait_next = (ids * (nwait + 1)) % E
    i = wait_next.argmin()
    print('bus', i, 'id', ids[i], 'waits', nwait[i], 'rounds, next in', wait_next[i], 'min')
    return ids[i] * wait_next[i]


def extended_gcd(a, b):
    """
    Find x, y such that ax + by = gcd(a, b).

    Returns:
        tuple of three numbers: x, y, gcd(a,b)
    """
    s, r = 0, b
    old_s, old_r = 1, a
    while r > 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s

    y = 0 if b == 0 else (old_r - old_s * a) // b
    return old_s, y, old_r


def diophantine_equation(a, b, c):
    """
    Solve Diophantine equation k * a ≡ c (mod b),
    which can be rewritten as k * a - b * l = c for some integer l.

    Returns:
        smallest integer k such that k * a ≡ c (mod b)
    """
    # for d = gcd(a, b), we first find x, y such that a * x + b * y = d
    x, y, d = extended_gcd(a, b)
    # Check if solution exists
    if c % d != 0:
        raise ValueError("No solution exists because gcd(a, b) does not divide c.")

    # Scale the solution to match c
    x0 = x * (c // d)
    # To find the smallest non-negative k, use modulo b/d
    mod = abs(b // d)  # Make sure mod is positive
    k = (x0 % mod + mod) % mod  # Ensure k is within the range [0, mod-1]
    return k, mod


def combine_congruences(congruences):
    """
    Combine multiple congruences of the form:
    k ≡ r_i (mod m_i)

    Parameters:
        congruences: List of tuples (r_i, m_i) representing each congruence.

    Returns:
        A tuple (k, M) where k is the smallest non-negative solution that satisfies all congruences,
        and M is the combined modulus.
    """
    # Start with the first congruence
    k, M = congruences[0]

    for i in range(1, len(congruences)):
        r_i, m_i = congruences[i]

        # Combine k ≡ r (mod M) and k ≡ r_i (mod m_i)
        # Solve M * x + k = r_i (mod m_i)
        x, _, gcd_mi_M = extended_gcd(M, m_i)

        # Ensure the difference is divisible by gcd
        if (r_i - k) % gcd_mi_M != 0:
            raise ValueError("No solution exists because moduli are not coprime and there's no common solution.")

        # Solve for x in M * x ≡ (r_i - k) / gcd (mod m_i / gcd)
        step = m_i // gcd_mi_M
        x0 = ((r_i - k) // gcd_mi_M) * x

        # New solution k, mod combined M
        k = (k + M * (x0 % step)) % (M * step)
        M *= step

    return k, M


def find_global_k(equations):
    """
    Find a global k that satisfies all the equations of the form:
    a_i * k = b_i * l_i + c_i, or equivalently a_i * k ≡ c_i (mod b_i).

    Parameters:
        equations: List of tuples (a_i, b_i, c_i)

    Returns:
        The smallest global k that satisfies all equations.
    """
    # Solve each equation and get its congruence form
    congruences = []
    for a, b, c in equations:
        k, m = diophantine_equation(a, b, c)
        congruences.append((k, m))

    # Combine all congruences to find a global k
    global_k, combined_modulus = combine_congruences(congruences)
    return global_k


def part2(data: DataType):
    """Solve part 2."""
    _, ids = data
    offsets = np.arange(ids.size)
    offsets = offsets[ids >= 0]
    ids = ids[ids >= 0]
    # we have t = k n0 for some k integer >= 0
    # for each i = 1, ..., N, we need to find li such that ni * l = n0 * k + i,
    # so li = (n0 * k + i) / ni an integer, <=> n0 * k ≡ -i (mod ni)
    n0, ids = ids[0], ids[1:]
    offsets = offsets[1:]

    # Equation n0 * k ≡ -i (mod ni) is called diophantine equation
    # we can find all ks for each equation and them combine them together
    k = find_global_k([
        (n0, ni, -i)
        for i, ni in zip(offsets, ids)
    ])
    t = n0 * k
    ls = (n0 * k + offsets) // ids
    assert ((ls * ids - offsets) == t).all()
    return t


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

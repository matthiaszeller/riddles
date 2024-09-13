"""
Inspired from https://github.com/iKevinY/advent/blob/main/2019/utils.py
"""

import re
import math
import hashlib
import operator
from contextlib import redirect_stdout
from functools import total_ordering, wraps, reduce
from io import StringIO
from pathlib import Path
from typing import Iterable, Any, Union

import numpy as np
from decorator import decorator

LETTERS = [x for x in 'abcdefghijklmnopqrstuvwxyz']
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)

# --- I/O ---

def load_riddle_files(caller_file: str) -> tuple[list[str], str]:
    fpath = Path(caller_file).parent
    with fpath.joinpath('examples.txt').open() as fh:
        examples = [
            block.strip('\n')
            for block in fh.read().split('§$@%')
        ]

    with fpath.joinpath('input.txt').open() as fh:
        data = fh.read()

    return examples, data


def line_parser(f):
    @wraps(f)
    def inner(input_data: str):
        return [f(line) for line in input_data.splitlines()]

    return inner


def parse_nums(line, negatives=True):
    num_re = r'-?\d+' if negatives else r'\d+'
    return [int(n) for n in re.findall(num_re, line)]


def parse_grid(grid: str) -> np.ndarray:
    return np.array(list(map(list, grid.splitlines())))


def print_grid(grid: np.ndarray | Iterable[Iterable[Any]]):
    print('\n'.join(''.join(line) for line in grid))


def capture_stdout(func, *args, discard=False, **kwargs):
    """Capture stdout from a function."""
    f = StringIO() if not discard else None
    with redirect_stdout(f):
        res = func(*args, **kwargs)
    return f.getvalue() if not discard else None, res


def print_formatted(text: str, color: str = None, bold: bool = False):
    color_code = {
        'r': '31', 'g': '32', 'b': '34', 'y': '33', 'p': '35', 'c': '36', 'w': '37',
    }.get(color, '0')
    bold_code = '1' if bold else '0'
    print(f'\033[{bold_code};{color_code}m{text}\033[0m')


# --- Other ---


def memoize(f):
    """Simple dictionary-based memoization decorator"""
    cache = {}

    def _mem_fn(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    _mem_fn.cache = cache
    return _mem_fn


def chunkify(lst, n: int):
    """Yield successive n-sized chunks from lst, where the last chunk may be smaller."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def all_unique(lst):
    return len(lst) == len(set(lst))


# --- Math ---


def factors(n):
    """Returns the factors of n."""
    return sorted(
        x for tup in (
            [i, n // i] for i in range(1, int(n ** 0.5) + 1)
            if n % i == 0)
        for x in tup)


def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a: np.ndarray):
    """Compute the lowest common multiple of elements of array"""
    return reduce(np.lcm, a)


def _eratosthenes(n):
    """http://stackoverflow.com/a/3941967/239076"""
    # Initialize list of primes
    _primes = [True] * n

    # Set 0 and 1 to non-prime
    _primes[0] = _primes[1] = False

    for i, is_prime in enumerate(_primes):
        if is_prime:
            yield i

            # Mark factors as non-prime
            for j in xrange(i * i, n, i):  # NOQA
                _primes[j] = False


def primes(n):
    """Return a list of primes from [2, n)"""
    return list(_eratosthenes(n))


# --- Hashing ---


def md5(msg):
    m = hashlib.md5()
    m.update(msg)
    return m.hexdigest()


def sha256(msg):
    s = hashlib.sha256()
    s.update(msg)
    return s.hexdigest()


def knot_hash(msg):
    lengths = [ord(x) for x in msg] + [17, 31, 73, 47, 23]
    sparse = range(0, 256)
    pos = 0
    skip = 0

    for _ in range(64):
        for l in lengths:
            for i in range(l // 2):
                x = (pos + i) % len(sparse)
                y = (pos + l - i - 1) % len(sparse)
                sparse[x], sparse[y] = sparse[y], sparse[x]

            pos = pos + l + skip % len(sparse)
            skip += 1

    hash_val = 0

    for i in range(16):
        res = 0
        for j in range(0, 16):
            res ^= sparse[(i * 16) + j]

        hash_val += res << ((16 - i - 1) * 8)

    return '%032x' % hash_val


HEX_DIRS = {
    'N': (1, -1, 0),
    'NE': (1, 0, -1),
    'SE': (0, 1, -1),
    'S': (-1, 1, 0),
    'SW': (-1, 0, 1),
    'NW': (0, -1, 1),
}


def hex_distance(x, y, z):
    """Returns a given hex point's distance from the origin."""
    return (abs(x) + abs(y) + abs(z)) // 2


# --- Point helper classes ---


def _cast_to_point_nd(items: Union[list, tuple, 'PointND', np.ndarray], expand_to=None):
    if isinstance(items, PointND):
        return items
    elif isinstance(items, (np.ndarray, list, tuple)):
        return PointND(*items)
    elif expand_to and isinstance(items, (float, int, np.int_, np.float_)):
        return expand_to.__class__(*(items, ) * expand_to.ndim)

    raise ValueError(f'cannot convert {items} to PointND')


@total_ordering
class PointND:
    """N-Dimensional Point. ***Not*** meant for computational efficiency, but for coding convenience."""

    def __init__(self, *coord):
        self.coords = coord

    @property
    def ndim(self) -> int:
        return len(self.coords)

    def _binop(self, op, other):
        other = _cast_to_point_nd(other, expand_to=self)
        return self.__class__(*(op(x, y) for x, y in zip(self.coords, other.coords)))

    def __add__(self, other):
        return self._binop(operator.add, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._binop(operator.sub, other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        return self._binop(operator.mul, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        return self._binop(operator.floordiv, other)

    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

    def __truediv__(self, other):
        return self._binop(operator.truediv, other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __eq__(self, other):
        return all(x == y for x, y in zip(self.coords, _cast_to_point_nd(other).coords))

    def __ne__(self, other):
        return any(x != y for x, y in zip(self.coords, _cast_to_point_nd(other).coords))

    def __str__(self):
        return f"({', '.join(map(str, self.coords))})"

    def __repr__(self):
        return f"{self.__class__.__name__}{self}"

    def __iter__(self):
        yield from self.coords

    def __hash__(self):
        return hash(tuple(self))

    def __lt__(self, other):
        return self.length < other.length

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, item):
        return self.coords[item]

    @property
    def manhattan(self):
        return sum(abs(c) for c in self.coords)

    @property
    def length(self):
        return math.sqrt(sum(c**2 for c in self.coords))

    def dist(self, other):
        return (self - other).length

    def dist_manhattan(self, other):
        return (self - other).manhattan

    def wrap_coords(self, grid_shape):
        return PointND(c % val for c, val in zip(self.coords, grid_shape))

    def is_within(self, shape):
        assert len(shape) == len(self.coords)
        return all(0 <= c < ub for c, ub in zip(self.coords, shape))

    def neighbours(self, shape=None, diag: bool = False, wrap: bool = False) -> list['PointND']:
        if self.ndim != 2:
            raise NotImplementedError

        pool = DIRS_8 if diag else DIRS_4
        neigh = [self + point for point in pool]

        if shape is not None:
            if wrap:
                neigh = [point.wrap_coords(shape) for point in neigh]
            else:
                neigh = [point for point in neigh if all(0 <= coord < ub for coord, ub in zip(point, shape))]

        return neigh


@total_ordering
class Point2D(PointND):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]


class Point3D(PointND):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]


DIRS_4 = [
    Point2D(0, 1),   # north
    Point2D(1, 0),   # east
    Point2D(0, -1),  # south
    Point2D(-1, 0),  # west
]

DIRS_8 = [
    Point2D(0, 1),    # N
    Point2D(1, 1),    # NE
    Point2D(1, 0),    # E
    Point2D(1, -1),   # SE
    Point2D(0, -1),   # S
    Point2D(-1, -1),  # SW
    Point2D(-1, 0),   # W
    Point2D(-1, 1),   # NW
]


# --- Bitwise operations ---


def _cast_to_uint(n: Union['_AbstractUInt', int, str], ref: '_AbstractUInt'):
    ref = ref.__class__
    if isinstance(n, _AbstractUInt):
        if n.__class__ != ref:
            raise NotImplementedError(f'Cannot cast {n.__class__} to {ref}')
        return n

    return ref.from_decimal(n)


@total_ordering
class _AbstractUInt:
    """Manipulation of bitwise arithmetics. ***Not*** meant for computational efficiency, but for convenience"""

    NBITS: int = None

    def __init__(self, value: int | str = 0):
        bits = value if isinstance(value, str) else bin(int(value))[2:]
        bits = bits.lstrip('0')
        assert len(bits) <= self.NBITS, f'Value {value} exceeds {self.NBITS} bits'
        self._bits = bits.zfill(self.NBITS)

    @property
    def bits(self) -> str:
        return self._bits

    def _bitwise_binop(self, op, other):
        other = _cast_to_uint(other, self)
        bit_string = (op(int(b1), int(b2)) for b1, b2 in zip(self._bits, other._bits))
        bit_string = map(str, bit_string)
        return self.__class__(''.join(bit_string))

    def _bitwise_op(self, op):
        bit_string = (op(int(b)) for b in self._bits)
        bit_string = map(str, bit_string)
        return self.__class__(''.join(bit_string))

    def _binop(self, op, other):
        res = op(int(self), int(other))
        if res < 0:
            raise NotImplementedError(f'Result of {self} {op} {other} (= {res}) is negative')
        elif res >= 2 ** self.NBITS:
            raise NotImplementedError(f'Result of {self} {op} {other} (= {res}) exceeds {self.NBITS} bits')

        return self.__class__.from_decimal(res)

    # Decimal operations
    def __add__(self, other):
        return self._binop(operator.add, other)

    def __sub__(self, other):
        return self._binop(operator.sub, other)

    def __mul__(self, other):
        return self._binop(operator.mul, other)

    # only implement // not /, as / may return float
    def __floordiv__(self, other):
        return self._binop(operator.floordiv, other)

    def __mod__(self, other):
        return self._binop(operator.mod, other)

    # Equality and comparison
    def __eq__(self, other):
        """Can only be True if other is of the same type (same number of bits)"""
        return self._bits == other.bits

    def __hash__(self):
        return hash(self._bits)

    # comparison could be more careful (signed integers, other not of same type), but this is good enough for now
    def __lt__(self, other):
        return int(self) < int(other)

    # Bitwise operations

    def __and__(self, other):
        return self._bitwise_binop(operator.and_, other)

    def __or__(self, other):
        return self._bitwise_binop(operator.or_, other)

    def __invert__(self):
        return self._bitwise_op(lambda b: int(not b))

    def __lshift__(self, n):
        n = int(n)
        return self.__class__(self._bits[n:] + '0' * n)

    def __rshift__(self, n):
        n = int(n)
        return self.__class__(self._bits[:-n])

    @classmethod
    def from_decimal(cls, value: int | str):
        return cls(bin(int(value))[2:])

    def __int__(self):
        return int(self._bits, 2)

    def __repr__(self):
        return f'{self.__class__.__name__}({int(self)})'


class UInt8(_AbstractUInt):
    NBITS = 8

class UInt16(_AbstractUInt):
    NBITS = 16

class UInt32(_AbstractUInt):
    NBITS = 32

class UInt64(_AbstractUInt):
    NBITS = 64


if __name__ == '__main__':
    Point2D(0, 0).neighbours(shape=(10, 10))

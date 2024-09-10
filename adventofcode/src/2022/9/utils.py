from pathlib import Path

import numpy as np

MOVES_MAP = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

Pos = tuple[int, int]


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    def parse_line(line: str):
        d, n = line.split()
        return d, int(n)

    return list(map(parse_line, data.splitlines()))


def update_tail(iH: int, jH: int, iT: int, jT: int) -> tuple[int, int]:
    def update_coord(coord: int, dist: int, abs_dist: int) -> int:
        if abs_dist == 0:
            return coord
        elif abs_dist == 2:
            sign = dist // abs_dist
            return coord + dist - sign
        else:
            return coord + dist

    di, dj = iH - iT, jH - jT
    adi, adj = abs(di), abs(dj)
    if adi < 2 and adj < 2:
        return iT, jT

    iT = update_coord(iT, di, adi)
    jT = update_coord(jT, dj, adj)

    return iT, jT


def print_history(history: list[tuple[tuple, tuple]], moves_only: list[tuple[str, int]] = None):
    positions = np.array(history)
    if moves_only is not None:
        indices = np.array([n for _, n in moves_only]).cumsum()
        positions = positions[indices]

    min_pos = positions.min(axis=(0, 1))
    positions -= min_pos.reshape(1, 1, 2)
    shape = positions.max(axis=(0, 1)) + 1

    grid = np.full(shape, '.')
    n_knots = positions.shape[1]
    labels = ['H'] + list(map(str, range(1, n_knots-1))) + ['T']
    for knots in positions:
        step = grid.copy()
        for knot, label in zip(knots[::-1], labels[::-1]):
            step[tuple(knot)] = label
        print('\n'.join(''.join(line) for line in step))
        print()


example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

example2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

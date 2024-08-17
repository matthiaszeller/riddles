import itertools

import numpy as np

from utils import *


# we must now expand while encoding positions, not handle the actual array

def expand(grid: np.ndarray, factor: int = 2):
    def update_pos(mask, axis, positions):
        idx_empty = np.argwhere(mask.all(axis)).squeeze(-1)
        for ii in range(len(idx_empty)):
            # the position of the empty array on this axis
            i = idx_empty[ii]
            # push galaxies that are beyond position i
            positions[positions > i] += factor - 1
            # update empty indices which are now outdated
            idx_empty[ii+1:] += factor - 1

        return len(idx_empty)

    mask_empty = grid == '.'
    positions = np.argwhere(~mask_empty)

    offset_row = update_pos(mask_empty, 1, positions[:, 0])
    offset_col = update_pos(mask_empty, 0, positions[:, 1])
    offset = np.array([offset_row, offset_col]) * (factor - 1)
    return positions, offset


def solve(grid: np.ndarray, factor: int = 2):
    positions, offset = expand(grid, factor)
    n = 0
    for p1, p2 in itertools.combinations(positions, 2):
        delta = np.abs(p2 - p1)
        n += delta.sum()

    return n


def print_grid(grid, expand_factor):
    pos, offset = expand(grid, expand_factor)
    shape = np.array(grid.shape) + offset
    grid = np.full(shape, '.')
    x, y = pos.T
    grid[x, y] = np.arange(1, len(pos) + 1)
    print(grid)


data = parse_data(example)
print(solve(data, 10))
print(solve(data, 100))
print(solve(parse_data(load_data()), 1_000_000))

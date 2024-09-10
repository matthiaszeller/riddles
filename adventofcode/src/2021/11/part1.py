import numpy as np
from scipy.signal import correlate

from utils import *


MASK = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def step(grid: np.ndarray):
    grid += 1
    mask = grid >= 10  # mask flags flashing octupuses
    has_flashed = np.full_like(mask, False)  # accumulate any octopus that flashed
    while mask.any():
        # propagate flashes
        neighbour_flashes = correlate(mask, MASK, mode='same')
        grid += neighbour_flashes

        has_flashed |= mask

        # some octupuses may still need to flash
        mask = (grid >= 10) & ~has_flashed

    # end of step: reset energy
    grid[has_flashed] = 0

    return has_flashed.sum()


def simulate_get_flashes(grid: np.ndarray, n: int = 100):
    final = grid.copy()
    total = sum(step(final) for _ in range(n))
    return final, total


data = parse_data(data)
final, n = simulate_get_flashes(data)


def simulate_sync(grid: np.ndarray):
    grid = grid.copy()
    N = np.prod(grid.shape)
    i = 0
    while True:
        i += 1
        n = step(grid)
        if n == N:
            return i, grid


n, final = simulate_sync(data)

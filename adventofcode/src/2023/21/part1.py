import numpy as np
from scipy.ndimage import convolve

from utils import *

MASK = np.zeros((3,3), dtype=int)
MASK[[0, 1, 1, 2], [1, 0, 2, 1]] = 1


def do_step(mask_rocks: np.ndarray, start: np.ndarray):
    mask_reached_tiles = convolve(start, MASK) > 0
    return mask_reached_tiles & ~mask_rocks


def solve(grid: np.ndarray, n: int):
    acc = [grid == 'S']
    mask_rocks = grid == '#'
    for _ in range(n):
        acc.append(do_step(mask_rocks, acc[-1]))

    return acc


data = parse_data(load_data())
sol = solve(data, 64)


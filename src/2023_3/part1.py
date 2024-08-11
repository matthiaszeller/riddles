from pathlib import Path

import numpy as np
from scipy.signal import convolve2d

from utils import *


def find_adjacent_numbers(grid: np.ndarray):
    # distinguish cell types
    mask_num = np.vectorize(str.isdigit)(grid)
    mask_dot = np.vectorize(lambda c: c == '.')(grid)
    mask_sym = ~mask_dot & ~mask_num
    # mark positions adjacent to symbols
    m = np.ones((3, 3))
    mask_adj = convolve2d(mask_sym, m, mode='same') > 0
    # find numbers
    nums = find_numbers(grid)
    # filter
    res = [
        (num, rows, cols)
        for (num, rows, cols) in nums
        if mask_adj[rows, cols].any()
    ]

    return res


def solve(grid):
    nums = find_adjacent_numbers(grid)
    nums, *_ = zip(*nums)
    return sum(nums)


data = parse_grid(example)
print(solve(data))

inp = get_data()
data = parse_grid(inp)
print(solve(data))

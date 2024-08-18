import numpy as np

from utils import *
from part1 import solve as solve1


def iter_start_config(grid: np.ndarray):
    n, m = grid.shape
    for i, direction in [(0, Direction.bottom), (n-1, Direction.top)]:
        for j in range(m):
            yield i, j, direction

    for j, direction in [(0, Direction.right), (m-1, Direction.left)]:
        for i in range(n):
            yield i, j, direction


def solve(grid: np.ndarray):
    energy = {}
    for i, j, direction in iter_start_config(grid):
        e = solve1(grid, (i, j), direction)
        energy[(i, j, direction)] = e.sum()

    return energy


data = parse_data(load_data())
sol = solve(data)
win = max(sol, key=lambda k: sol[k])
print(win, sol[win])

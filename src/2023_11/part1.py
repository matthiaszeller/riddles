import itertools

import numpy as np

from utils import *


def expand(grid: np.ndarray) -> np.ndarray:
    def insert(lst: list, indices):
        offset = 0
        for i in indices:
            i += offset
            lst.insert(i, lst[i])
            offset += 1

    mask = grid != '#'
    empty_rows = np.argwhere(mask.all(axis=1)).squeeze()
    rows = list(grid)
    insert(rows, empty_rows)

    empty_cols = np.argwhere(mask.all(axis=0)).squeeze()
    grid = np.array(rows)
    cols = list(grid.T)
    insert(cols, empty_cols)
    grid = np.array(cols).T

    return grid


def number_galaxies(grid: np.ndarray) -> np.ndarray:
    mask = grid == '#'
    nums = np.arange(1, mask.sum() + 1)
    x, y = np.where(mask)
    grid = grid.copy()
    grid[x, y] = nums
    return grid


def shortest_path_pair(pos1, pos2):
    delta = pos2 - pos1
    return np.abs(delta).sum()


def shortest_paths(grid: np.ndarray):
    mask = grid != '.'
    pos = np.argwhere(mask)
    dist = []
    for pos1, pos2 in itertools.combinations(pos, 2):
        label1 = grid[tuple(pos1)]
        label2 = grid[tuple(pos2)]
        dist.append((label1, label2, shortest_path_pair(pos1, pos2)))

    return dist


def solve(grid: np.ndarray):
    grid = expand(grid)
    dist = shortest_paths(grid)
    return sum([d for _, _, d in dist])


data = parse_data(example)
print(solve(data))

print(solve(parse_data(load_data())))

import numpy as np
from scipy.ndimage import binary_fill_holes

from utils import *


def parse_data(data: str):
    def parse_line(line: str):
        a, b, c = line.split(' ')
        b = int(b)
        c = c.strip('()')
        return a, b, c

    return list(map(parse_line, data.splitlines()))


def dig(steps: list, pos=(0, 0)):
    def inner(pos, direction, m, color):
        i, j = pos
        for _ in range(m):
            if direction == 'R':
                j += 1
            elif direction == 'D':
                i += 1
            elif direction == 'L':
                j -= 1
            else:
                i -= 1

            digs[(i, j)] = color

        return i, j

    digs = {pos: None}
    for direction, n, col in steps:
        pos = inner(pos, direction, n, col)

    return digs


def dig2grid(digs: dict):
    def process_dimension(indices: np.ndarray):
        lower = indices.min()
        assert lower <= 0
        indices = indices - lower
        upper = indices.max() + 1
        return indices, upper

    keys = list(digs)
    i, j = np.array(keys).T
    i, m = process_dimension(i)
    j, n = process_dimension(j)
    grid = np.full((m, n), False)
    grid[i, j] = True
    return grid


def fill_holes(grid: np.ndarray):
    return binary_fill_holes(grid)


data = parse_data(load_data())
digs = dig(data)
grid = dig2grid(digs)
filled = fill_holes(grid)

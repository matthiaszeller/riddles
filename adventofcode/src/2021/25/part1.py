

from utils import *


def step(grid: np.ndarray):
    def move(mask, mask_any, axis, char):
        mask_move = np.roll(~mask_any, -1, axis) & mask
        idx = np.argwhere(mask_move).T
        grid[tuple(idx)] = '.'
        idx[axis] = (idx[axis] + 1) % grid.shape[axis]
        grid[tuple(idx)] = char


    mask_east = grid == '>'
    mask_south = grid == 'v'
    mask_any = mask_south | mask_east

    move(mask_east, mask_any, 1, '>')

    mask_any = (grid == '>') | mask_south
    move(mask_south, mask_any, 0, 'v')


def move_until_stop(grid: np.ndarray):
    prev = np.full_like(grid, '.')
    grid = grid.copy()
    n = 0
    while (prev != grid).any():
        prev = grid.copy()
        step(grid)
        n += 1

    return n


grid = parse_data(load_data())
print(move_until_stop(grid))

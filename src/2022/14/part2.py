import numpy as np

from utils import *


def print_grid(grid):
    print('\n'.join(''.join(row) for row in grid))


def solve(grid: np.ndarray, src: tuple[int, int], max_produce: int = int(1e6)):
    # pad each side with air
    height = grid.shape[0] + 2  # +2 for the floor and layer of air
    pad_width = height + 2
    grid = np.pad(grid, ((0, 0), (pad_width, pad_width)), 'constant', constant_values='.')
    # add floor and layer of air
    grid = np.concatenate((
        grid,
        np.full((1, grid.shape[1]), '.'),
        np.full((1, grid.shape[1]), '#'),
    ))
    # shift the source position w.r.t. padding
    src = (src[0], src[1]+pad_width)
    # we track when to produce sand with a variable giving position of currently-moving block
    moving_sand = None
    finished = False
    n_produced = 0
    while not finished:
        # produce sand if needed
        if moving_sand is None:
            if n_produced >= max_produce:
                break

            moving_sand = np.array(src)
            n_produced += 1

        # explore moves in this order: down, down-left, down-right
        for delta in [(1, 0), (1, -1), (1, 1)]:
            candidate = moving_sand + delta
            match grid[tuple(candidate)]:
                case '.':
                    moving_sand = candidate
                    do_rest = False
                    break
                case _:
                    do_rest = True

        if do_rest:
            grid[tuple(moving_sand)] = 'o'
            if (moving_sand == src).all():
                finished = True
            moving_sand = None

    return grid, n_produced


data = parse_data(load_data())
grid, shift, src = build_grid(data)
grid, n = solve(grid, src, )
print_grid(grid)
print(n)

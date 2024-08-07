from copy import deepcopy

import data
from utils import *


def tilt_north(grid):
    nrow, ncol = len(grid), len(grid[0])
    grid = deepcopy(grid)
    # scan from top to bottom
    for j in range(ncol):
        for i in range(nrow):
            # find (if any) the rolling rock that will roll to pos (i, j)
            # once found, stop because a given position can have only 1 rock

            # if (i, j) is not empty, nothing will roll here
            if grid[i][j] != '.':
                continue

            # find any rolling rock below
            for ii in range(i+1, nrow):
                if grid[ii][j] == '#':
                    break
                elif grid[ii][j] == 'O':
                    # the round rock will roll straight to (i, j)
                    grid[i][j], grid[ii][j] = 'O', '.'
                    break

    return grid


grid = parse_grid(data.example)


print_grid(grid)


print()
tilted = tilt_north(grid)
print_grid(tilted)

print(tilted == parse_grid(data.example_titled_north))
print(compute_total_load(tilted))
print()
grid = parse_grid(data.data)

tilted = tilt_north(grid)

load = compute_total_load(tilted)
print(load)

import numpy as np

from utils import *


def solve(jets: str, n: int, augment_grid_step: int = 500):
    rock_factory = get_rock_factory()
    jets_iter = get_iter_jets(jets)
    grid = create_grid()
    highest_rock_height = grid.shape[0] - 1
    heights = []
    for _ in range(n):
        rock: np.ndarray = rock_factory(highest_rock_height)

        # Handle grid height
        if (rock < 0).any():
            grid = augment_grid(grid, rows=augment_grid_step)
            rock += np.array([[augment_grid_step, 0]])
            highest_rock_height += augment_grid_step

        rest = False
        while not rest:
            # Move from jet
            delta_pos: np.ndarray = next(jets_iter)
            candidate_rock = rock + delta_pos
            # only let rock be pushed by jet if it doesn't collide with walls / resting rocks
            if not (grid[tuple(candidate_rock.T)] == '#').any():
                rock = candidate_rock

            # Fall down
            candidate_rock = rock + np.array([1, 0])
            if (grid[tuple(candidate_rock.T)] == '#').any():
                rest = True
            else:
                rock = candidate_rock

        # rock is resting, add it to grid
        grid[tuple(rock.T)] = '#'

        # update tower height
        last_rock_height = rock[:, 0].min()
        highest_rock_height = min(last_rock_height, highest_rock_height)
        heights.append(grid.shape[0] - highest_rock_height - 1)

    return grid, np.array(heights)


if __name__ == '__main__':
    grid, h = solve(example, 2022)


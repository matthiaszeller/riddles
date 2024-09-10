import itertools
from pathlib import Path

import numpy as np

_ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

RockType = np.ndarray


def _parse_rock(rock: str) -> RockType:
    rock = np.array([list(line) for line in rock.splitlines()])
    rock = rock == '#'
    return np.argwhere(rock)


ROCKS: list[RockType] = list(map(_parse_rock, _ROCKS.split('\n\n')))


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def get_rock_factory():
    rock_generator = itertools.cycle(ROCKS)

    def inner(highest_rock_i: int) -> RockType:
        j = 3
        i = highest_rock_i - 4

        rock = next(rock_generator)
        rock_height = rock[-1, 0]

        return rock + np.array([[i-rock_height, j]])

    return inner


def get_iter_jets(jets: str):
    for jet in itertools.cycle(jets):
        if jet == '>':
            yield np.array([0, 1])
        else:
            yield np.array([0, -1])


def create_grid(init_height: int = 20) -> np.ndarray:
    grid = np.full((init_height, 7), '.')
    grid = np.pad(grid, ((0, 1), (1, 1)), 'constant', constant_values='#')
    return grid


def augment_grid(grid: np.ndarray, rows: int = 50):
    return np.concatenate((
        np.pad(
            np.full((rows, 7), '.'),
            ((0, 0), (1, 1)),
            'constant',
            constant_values='#'
        ),
        grid
    ))


def get_rock_indices(rock: np.ndarray, i: int, j: int):
    mask = rock != '.'
    ii, jj = mask.nonzero()
    return ii+i, jj+j


def print_grid(grid: np.ndarray, rock: RockType = None, rock_char: str = '@'):
    grid = grid.copy()

    if rock is not None:
        grid[tuple(rock.T)] = rock_char

    grid[-1, :] = ['+'] + ['-'] * (grid.shape[1] - 2) + ['+']
    grid[:-1, [0, -1]] = '|'
    n = grid.shape[0]
    digits = len(str(n))
    for i, line in enumerate(grid):
        print(f'{i:<{digits}}', ''.join(line))


def get_tower_height(grid: np.ndarray) -> int:
    highest_rock = (grid[:-1, 1:-1] == '#').any(axis=1).nonzero()[0].min()
    return grid.shape[0] - highest_rock - 1


example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

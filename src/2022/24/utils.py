from pathlib import Path

import numpy as np
from numpy.core.numeric import full_like

BLIZZARD_MAPPING = {
    '^': np.array([-1, 0]),
    '>': np.array([0, 1]),
    'v': np.array([1, 0]),
    '<': np.array([0, -1]),
}


class Grid:

    start = (1, 1)

    def __init__(self, m: int, n: int, directions: np.ndarray, positions: np.ndarray):
        self.m = m
        self.n = n
        self.directions = directions
        self.positions = positions

    @property
    def end(self) -> tuple[int, int]:
        return self.m-2, self.n-2

    def copy(self) -> 'Grid':
        return Grid(self.m, self.n, self.directions, self.positions.copy())

    def to_grid(self) -> np.ndarray:
        grid = np.full((self.m-4, self.n-2), '.')
        # handle grid boundaries
        grid = np.pad(grid, ((2, 2), (1, 1)), constant_values='#')
        grid[[1, -2], [1, -2]] = '.'
        # put blizzards
        grid[tuple(self.positions.T)] = self.directions
        # handle superimposing blizzards
        unique_positions, counts = np.unique(self.positions, return_counts=True, axis=0)
        mask = counts > 1
        grid[tuple(unique_positions[mask].T)] = counts[mask].astype(str)

        return grid

    def to_empty_mask(self):
        """Mask of empty positions (no blizzard and no walls)"""
        mask = np.full((self.m, self.n), True)
        mask[[0, 1, -1, -2], :] = False
        mask[:, [0, -1]] = False
        mask[[1, -2], [1, -2]] = True
        mask[tuple(self.positions.T)] = False
        return mask

    def move_blizzards(self, in_place: bool = False) -> 'Grid':
        new_pos = move_blizzards(self.directions, self.positions, (self.m, self.n))
        if in_place:
            self.positions = new_pos
            grid = self
        else:
            grid = self.copy()
            grid.positions = new_pos

        return grid

    def __repr__(self):
        return str(self.to_grid())

    @classmethod
    def from_grid(cls, grid: np.ndarray) -> 'Grid':
        m, n = grid.shape
        mask = np.full((m, n), False)
        for char in BLIZZARD_MAPPING:
            mask |= grid == char

        positions = np.argwhere(mask)
        directions = grid[tuple(positions.T)]
        return Grid(m, n, directions, positions)


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    grid = np.array([
        list(line) for line in data.splitlines()
    ])
    return np.pad(grid, ((1, 1), (0, 0)), constant_values='#')


# Doesn't work for:
#   * superimposing blizzards
#   * not implemented boundary conditions
#
# def move_blizzard(grid: np.ndarray):
#     m, n = grid.shape
#     delta_pos = np.zeros((m, n, 2), dtype=int)
#     for char, delta in BLIZZARD_MAPPING.items():
#         mask = grid == char
#         delta_pos[mask] = delta
#
#     x, y = np.meshgrid(np.arange(m), np.arange(n), indexing='ij')
#     new_x = x + delta_pos[..., 0]
#     new_y = y + delta_pos[..., 1]
#
#     mask = (delta_pos > 0).any(axis=-1)
#     new_grid = grid.copy()
#     # clear blizzard pixels that will move
#     new_grid[mask] = '.'
#     new_grid[new_x[mask], new_y[mask]] = grid[mask]
#     return new_grid


def move_blizzards(blizzards: np.ndarray, positions: np.ndarray, shape: tuple[int, int]):
    delta_pos = np.full_like(positions, -1)
    for char, delta in BLIZZARD_MAPPING.items():
        mask = blizzards == char
        delta_pos[mask] = delta

    new_pos = positions + delta_pos

    # Boundary wrapping
    for axis, size in zip((0, 1), shape):
        min_edge = 1 - axis
        max_edge = size - 1 - (1 - axis)

        mask = new_pos[:, axis] == max_edge
        new_pos[mask, axis] = min_edge+1

        mask = new_pos[:, axis] == min_edge
        new_pos[mask, axis] = max_edge-1

    return new_pos


def cropped_view(mask: np.ndarray, position: tuple[int, int]):
    view = np.full((3, 3), False)
    indices = np.array([-1, 0, 1])
    x, y = np.meshgrid(indices + position[0], indices + position[1], indexing='ij')
    m, n = mask.shape
    valid = (x >= 0) & (x < m) & (y >= 0) & (y < n)
    view[valid] = mask[x[valid], y[valid]]
    indices = np.stack((x, y), axis=-1)

    return view, indices


example1 = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

example2 = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

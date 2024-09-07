from pathlib import Path

import numpy as np


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str) -> tuple[list[tuple[int, int]], list[tuple[str, int]]]:
    coords, folds = data.split('\n\n')
    coords = [tuple(map(int, line.split(','))) for line in coords.splitlines()]
    folds = map(lambda e: e.split()[-1].split('='), folds.splitlines())
    folds = [(tpl[0], int(tpl[1])) for tpl in folds]

    return coords, folds


def build_grid(coords: list[tuple[int, int]]):
    coords = np.array(coords)
    # first coord is horizontal
    coords = np.roll(coords, shift=1, axis=1)
    shape = coords.max(axis=0) + 1
    grid = np.full(shape, False)
    grid[tuple(coords.T)] = True
    return grid


def print_grid(grid: np.ndarray):
    grid_print = np.full(grid.shape, '.')
    grid_print[grid] = '#'
    print('\n'.join(''.join(line) for line in grid_print))


example = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
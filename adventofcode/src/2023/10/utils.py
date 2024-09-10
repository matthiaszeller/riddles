from pathlib import Path

import numpy as np


PIPES = {
    '|', '-', 'L', 'J', '7', 'F', 'S'
}
PIPES_CONNECT = {
    '|': {'t': True, 'b': True},
    '-': {'l': True, 'r': True},
    'L': {'t': True, 'r': True},
    'J': {'l': True, 't': True},
    '7': {'l': True, 'b': True},
    'F': {'b': True, 'r': True},
    'S': {'l': True, 't': True, 'r': True, 'b': True}
}


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> np.ndarray:
    a = np.array([
        [c for c in line]
        for line in data.splitlines()
    ])
    return np.pad(a, pad_width=(1, 1), mode='constant', constant_values='.')


def find_start(grid: np.ndarray):
    (i, j), = np.argwhere(grid == 'S')
    return i, j


def find_connected_pipes(grid: np.ndarray, i: int, j: int):
    # mask
    connect = PIPES_CONNECT[grid[i, j]]
    mask = np.array([
        connect.get('l', False), connect.get('t', False),
        connect.get('b', False), connect.get('r', False)
    ])
    # relative indices for left, top, bottom, right
    rel_ind = np.arange(-1, 2)
    adj_id_x, adj_id_y = [1, 0, 2, 1], [0, 1, 1, 2]
    xx = rel_ind[adj_id_x][mask]
    yy = rel_ind[adj_id_y][mask]
    # absolute indices
    x = xx + i
    y = yy + j
    for ii, jj in zip(x, y):
        if grid[ii, jj] in PIPES:
            yield ii, jj

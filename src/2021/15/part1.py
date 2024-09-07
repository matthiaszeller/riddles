import networkx as nx
import numpy as np

from utils import *


def build_graph(grid: np.ndarray):
    def is_valid(i: int, j: int) -> bool:
        return 0 <= i < m and 0 <= j < n

    G = nx.DiGraph()
    m, n = grid.shape

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ii, jj = i+di, j+dj
                if not is_valid(ii, jj):
                    continue

                G.add_edge((i, j), (ii, jj), w=grid[ii, jj])

    return G, (0, 0), (grid.shape[0]-1, grid.shape[1]-1)


def print_path(grid: np.ndarray, path: list[tuple[int, int]]):
    coords = np.array(path)
    # use bold modifiers to print the path
    before, after = '\033[1m', '\033[0m'
    num_chars = 1 + len(before) + len(after)
    dtype = np.dtype(f'<U{num_chars}')

    grid = grid.astype(dtype)
    gbefore = np.full_like(grid, '')
    gbefore[tuple(coords.T)] = before
    gafter = np.full_like(grid, '')
    gafter[tuple(coords.T)] = after

    grid = np.char.add(gbefore, grid)
    grid = np.char.add(grid, gafter)
    print('\n'.join(''.join(line) for line in grid))


if __name__ == '__main__':

    data = parse_data(load_data())
    G, start, end = build_graph(data)
    path = nx.shortest_path(G, start, end, weight='w')
    L = nx.shortest_path_length(G, start, end, weight='w')

    print_path(data, path)

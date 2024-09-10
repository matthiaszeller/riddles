from pathlib import Path

import numpy as np

example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


NEXT_MOVES = {
    '>': [(0, 1)],
    '<': [(0, -1)],
    '^': [(-1, 0)],
    'v': [(1, 0)],
    '.': [(1, 0), (-1, 0), (0, 1), (0, -1)]
}


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> np.ndarray:
    return np.array(list(map(list, data.splitlines())))


def iter_path_tiles(grid: np.ndarray, pos):
    i, j = pos
    if i == grid.shape[0]-1:
        return

    for di, dj in NEXT_MOVES[grid[pos]]:
        next_tile = grid[i+di, j+dj]
        if next_tile == '#':
            continue
        elif next_tile == '.':
            yield i+di, j+dj
            continue

        (ii, jj) = NEXT_MOVES[next_tile][0]
        # -(ii, jj) is the forbidden source tile
        if (-ii, -jj) != (di, dj):
            yield i+di, j+dj


def find_start(grid: np.ndarray) -> tuple[int, int]:
    (j, ), = np.where(grid[0] == '.')
    return 0, j


def factory_iter_edges(grid: np.ndarray, start):
    grid = np.pad(grid, (1, 1), mode='constant', constant_values='#')
    mask_path = grid != '#'
    idx_padded = np.argwhere(mask_path)

    def inner():
        for pos in idx_padded:
            neigh = set(iter_path_tiles(grid, pos))
            neigh.difference_update()


if __name__ == '__main__':
    grid = np.array([
        ['.', 'v', '.'],
        ['>', '.', '>'],
        ['#', '#', '.']
    ])
    print(list(iter_path_tiles(grid, (1, 1))))

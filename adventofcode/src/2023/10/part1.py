from collections import namedtuple

import numpy as np

from utils import *


example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

example2 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""


class LoopCell:

    def __init__(self, i: int, j: int, prev: 'LoopCell' = None, next: 'LoopCell' = None):
        self.i = i
        self.j = j
        self.prev = prev
        self.next = next

    def __repr__(self):
        arrow = f'<->' if (self.prev and self.next) else ('->' if self.next else '<-')
        return f'LoopCell(i={self.i}, j={self.j}, {arrow})'


def explore_loop(grid: np.ndarray, i: int, j: int):
    unexplored = {LoopCell(i, j)}
    explored: dict[tuple[int, int], LoopCell] = {}
    last = (i, j)
    while len(unexplored) > 0:
        cell = unexplored.pop()
        explored[(cell.i, cell.j)] = cell

        for explore_pos in find_connected_pipes(grid, cell.i, cell.j):
            if explore_pos not in explored:
                last = explore_pos
                new_cell = LoopCell(*explore_pos, prev=cell)
                cell.next = new_cell
                unexplored.add(new_cell)
                # several connected piplines only possible with S,
                # it's fine to just explore in a single direction
                break

    # connect the starting cell (i, j) with the last cell explore_pos
    # start has no prev, last has no next
    first, last = explored[(i, j)], explored[last]
    first.prev = last
    last.next = first

    return explored


def find_loop(grid: np.ndarray, i: int = None, j: int = None):
    if i is None:
        i, j = find_start(grid)

    explored = explore_loop(grid, i, j)
    assert all(cell.next and cell.prev for cell in explored.values())
    start_cell = explored[(i, j)]
    return start_cell


def get_distances(start: LoopCell):
    explored = {}
    unexplored = {start}
    distance = -1
    while len(unexplored) > 0:
        tmp = set()
        distance += 1
        for cell in unexplored:
            explored[cell] = distance
            if cell.next not in explored:
                tmp.add(cell.next)
            if cell.prev not in explored:
                tmp.add(cell.prev)

        unexplored = tmp

    return explored


def print_distances(grid: np.ndarray, distances: dict[LoopCell, int]):
    grid = np.full_like(grid, '.')
    for cell, dist in distances.items():
        grid[cell.i, cell.j] = dist

    print(grid)


def replace_start(grid: np.ndarray):
    i, j = find_start(grid)

    # connections the elements are allows to have with start
    allowed_connections = {
        (0, -1): 'r',  # left element must have right connection
        (-1, 0): 'b',  # top element must have bottom connection
        (0, 1):  'l',  # right element must have left connection
        (1, 0):  't',  # bottom element must have top connection
    }

    connections = set()
    for ii, jj in find_connected_pipes(grid, i, j):
        dx, dy = ii - i, jj - j
        required_connection = allowed_connections[(dx, dy)]
        is_connected = PIPES_CONNECT[grid[ii, jj]].get(required_connection, False)
        if is_connected:
            connections.add(required_connection)

    replace_map = [
        ({'l', 't'}, 'F'),
        ({'t', 'r'}, '7'),
        ({'l', 'r'}, '-'),
        ({'t', 'b'}, '|'),
        ({'b', 'r'}, 'J'),
        ({'b', 'l'}, 'L')
    ]
    replace = set()
    for sub, r in replace_map:
        if sub.issubset(connections):
            replace.add(r)

    assert len(replace) == 1
    grid[i, j] = next(iter(replace))

    return i, j


def solve(grid):
    i, j = replace_start(grid)
    start = find_loop(grid, i, j)
    dist = get_distances(start)
    return max(dist.values())


if __name__ == '__main__':
    print(solve(parse_data(load_data())))

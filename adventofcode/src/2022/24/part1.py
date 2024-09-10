import heapq
from collections import defaultdict
from time import time

from utils import *


# Strategy:
#   * manipulate grid with walls padded on top and bottom to avoid boundary conditions when moving
#   * due to superimposition of blizzards, easier to store their position and wind direction in numpy arrays
#       -> dedicated class Grid
#   * the core algorithm uses a priority queue to explore possible moves, with heuristic being distance to destination


CANDIDATE_MOVES = np.array([
    [False, True, False],
    [True, True, True],
    [False, True, False]
])


def get_candidate_positions(grid: Grid, current_pos: tuple[int, int]):
    i, j = current_pos
    mask_free = grid.to_empty_mask()[i-1:i+2, j-1:j+2]
    mask_candidates = mask_free & CANDIDATE_MOVES
    x, y = mask_candidates.nonzero()
    yield from zip(x+(i-1), y+(j-1))  # the -1 is because the 3x3 mask is centered at (1, 1)


class GridDict(defaultdict[int, Grid]):

    def __missing__(self, key: int):
        assert key-1 in self
        g = self[key-1].move_blizzards()
        self[key] = g
        return g


Pos = tuple[int, int]


def solve(grid: Grid, start: Pos = None, end: Pos = None, initial_time: int = 0):
    """Modified dijsktra algorithm"""
    def get_destination_dist(i: int, j: int) -> int:
        return abs(end_i - i) + abs(end_j - j)

    def push_queue(time: int, position: Pos):
        h = get_destination_dist(*position)
        heapq.heappush(Q, (time, h, position))

    def pop_queue() -> tuple[int, Pos]:
        time, _, pos = heapq.heappop(Q)
        return time, pos

    # * cost of each move is 1 unit of time
    # * edge availability is dynamic
    # * returning (at later time) to an already visited position might be optimal / necessary
    # => state of the algo is (position, time)

    start = grid.start if start is None else start
    (end_i, end_j) = grid.end if end is None else end

    grids = GridDict()
    grids[initial_time] = grid
    # min-priority queue of tuples (time, distance_to_end, position)
    # in python, tuples are compared by position, so priority is first on time then distance_to_end
    # distance_to_end is just a heuristic to hopefully speed things up
    Q: list[tuple[int, int, Pos]] = []
    # record for having O(1) lookup of visited states
    # if two paths reach the same position at the same time, they have the same cost,
    # so we only need 1 predecessor
    previous: dict[tuple[int, Pos], tuple[int, Pos]] = {}

    push_queue(time=initial_time, position=start)

    last = None
    n = 0
    while len(Q) > 0:
        t, pos = pop_queue()
        # due to priority queue prioritizing time, whenever we reach the end -> optimal
        if pos == (end_i, end_j):
            last = (t, pos)
            break

        # advance time
        t += 1
        n += 1

        grid_t = grids[t]  # get blizzard states at next time

        candidates = get_candidate_positions(grid_t, pos)
        for new_pos in candidates:
            if (t, new_pos) not in previous:
                push_queue(t, new_pos)
                previous[(t, new_pos)] = (t-1, pos)

    return n, last, previous, grids


def backtrack(last: tuple[int, Pos], previous: dict):
    path = []
    current = last
    while current is not None:
        path.append(current)
        current = previous.get(current)

    return path[::-1]


if __name__ == '__main__':
    grid = parse_data(load_data())
    grid = Grid.from_grid(grid)
    dt = time()
    n, last, previous, grids = solve(grid)
    path = backtrack(last, previous)
    dt = time() - dt

    print(f'optimal solution at t={path[-1][0]} found in {dt:.3} s in {n} iterations')

# for (time, pos) in path:
#     print('-' * 10, 'time', time)
#     g = grids[time].to_grid()
#     g[pos] = 'E'
#     print('\n'.join(''.join(line) for line in g))

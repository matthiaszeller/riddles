

from utils import *


def solve(grid: np.ndarray, start_pos=(0, 0), start_direction=Direction.right):
    n, m = grid.shape

    def isin(pos):
        i, j = pos
        return (0 <= i < n) and (0 <= j < m)

    energized = np.full(grid.shape, False)
    beams = [(np.array(start_pos), start_direction)]
    history: set[tuple[int, int, Direction]] = set()
    while len(beams) > 0:
        pos, dir = beams.pop()
        # avoid loops
        history_item = tuple(pos) + (dir,)
        if history_item in history:
            continue
        history.add(history_item)

        energized[tuple(pos)] = True
        tile = grid[tuple(pos)]
        for next_dir in next_directions(tile, dir):
            next_pos = pos + next_dir.value
            if isin(next_pos):
                beams.append((next_pos, next_dir))

    return energized


if __name__ == '__main__':
    data = parse_data(load_data())
    e = solve(data)

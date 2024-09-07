

from utils import *


def fold(grid: np.ndarray, axis: str, idx: int):
    axis = 0 if axis == 'y' else 1
    assert (grid.take(indices=idx, axis=axis) != '#').all()

    axis_size = grid.shape[axis]
    axis_size_folded = (axis_size - 1) // 2
    part1 = grid.take(range(axis_size_folded), axis=axis)
    part2 = grid.take(range(axis_size_folded+1, axis_size), axis=axis)
    # fold part 2
    part2 = np.flip(part2, axis=axis)

    final = part1 | part2
    return final


def solve(coords, folds):
    grid = build_grid(coords)
    grids = [grid]
    for axis, n in folds:
        grid = fold(grid, axis, n)
        grids.append(grid)

    return grids


coords, folds = parse_data(load_data())
grids = solve(coords, folds)


from utils import *


def solve(grid: np.ndarray, src: tuple[int, int], max_produce: int = int(1e6)):
    # add a row to flag the abyss
    grid = np.pad(grid, ((0, 1), (1, 1)), mode='constant', constant_values='x')
    # shift the source position w.r.t. padding
    src = (src[0], src[1]+1)
    # we track when to produce sand with a variable giving position of currently-moving block
    moving_sand = None
    finished = False
    n_produced = 0
    while not finished:
        # produce sand if needed
        if moving_sand is None:
            if n_produced >= max_produce:
                break

            moving_sand = np.array(src)
            n_produced += 1

        # explore moves in this order: down, down-left, down-right
        do_rest = False
        for delta in [(1, 0), (1, -1), (1, 1)]:
            candidate = moving_sand + delta
            match grid[tuple(candidate)]:
                case '.':
                    moving_sand = candidate
                    do_rest = False
                    break
                case 'x':
                    finished = True
                    break
                case _:
                    do_rest = True

        if not finished and do_rest:
            grid[tuple(moving_sand)] = 'o'
            moving_sand = None

    return grid, n_produced - 1  # the last sand block fell into abyss


data = parse_data(load_data())
grid, shift, src = build_grid(data)
grid, n = solve(grid, src, )
print(grid)
print(n)



def parse_grid(data):
    return [list(line) for line in data.split("\n")]


def print_grid(grid, indices: bool = True):
    nrow, ncol = len(grid), len(grid[0])
    for i in range(nrow):
        if indices:
            print(f"{i:2d} ", end="")
        print("".join(grid[i]))
    if indices:
        print("   ", end="")
    print("".join(str(j % 10) for j in range(ncol)))


def print_grid_side(*grids):
    for lines in zip(*grids):
        print("   ".join("".join(line) for line in lines))


def compute_total_load(grid):
    nrow, ncol = len(grid), len(grid[0])
    S = 0
    for i in range(nrow):
        L = ncol - i
        for j in range(ncol):
            if grid[i][j] == 'O':
                S += L

    return S
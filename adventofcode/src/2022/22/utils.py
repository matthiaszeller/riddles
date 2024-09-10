from pathlib import Path

import numpy as np


MAP_FACING = {
    '^': np.array([-1, 0]),
    '>': np.array([0, 1]),
    '<': np.array([0, -1]),
    'v': np.array([1, 0]),
}

MAP_FACING_RIGHT = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}
MAP_FACING_LEFT = {
    '^': '<',
    '<': 'v',
    'v': '>',
    '>': '^'
}


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    world, instr_raw = data.split('\n\n')

    instr = []
    tmp = ''
    for i in instr_raw:
        if i.isdigit():
            tmp += i
        else:
            instr.append(int(tmp))
            tmp = ''
            instr.append(i)
    instr.append(int(tmp))

    world = world.replace(' ', '~')
    lines = [list(line) for line in world.splitlines()]
    n_col = max(map(len, lines))

    world = np.stack([
        np.array(line + ['~'] * (n_col - len(line)))
        for line in lines
    ])
    return np.pad(world, 1, constant_values='~'), instr


def next_pos_factory(grid: np.ndarray):
    def get_wrapping_indices(values: np.ndarray):
        idx, = values.nonzero()
        if len(idx) == 0:
            return -1, -1

        return idx[0], idx[-1]

    mask = grid == '~'
    rows_wrapping = [
        get_wrapping_indices(row)
        for row in (~mask)
    ]
    cols_wrapping = [
        get_wrapping_indices(col)
        for col in (~mask).T
    ]

    def inner(i: int, j: int, facing: str) -> tuple[int, int] | None:
        i2, j2 = MAP_FACING[facing] + (i, j)
        if mask[i2, j2]:
            if i == i2:  # wrap on horizontal axis (1)
                i2 = i
                a, b = rows_wrapping[i]
                j2 = a if facing == '>' else b
            else:
                j2 = j
                a, b = cols_wrapping[j]
                i2 = a if facing == 'v' else b

        tile = grid[i2, j2]
        assert tile != '~'
        if tile == '#':
            return None

        return i2, j2

    # take account padding for starting pos
    start = 1, rows_wrapping[1][0]

    return start, inner


def print_map(grid: np.ndarray):
    grid = grid[1:-1, 1:-1]
    print('\n'.join(''.join(line) for line in grid))


def next_facing(facing: str, turn: str):
    mapping = MAP_FACING_LEFT if turn == 'L' else MAP_FACING_RIGHT
    return mapping[facing]


example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

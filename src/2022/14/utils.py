from pathlib import Path

import numpy as np


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    def parse_line(line):
        points = line.split(' -> ')
        return np.roll(np.array(list(map(eval, points))), 1, axis=1)

    return list(map(parse_line, data.splitlines()))


def build_grid(data):
    def draw(i1: int, j1: int, i2: int, j2: int):
        horizontal = i1 == i2
        if horizontal:
            jstart, jend = sorted((j1, j2))
            grid[i1, jstart-shift_j:jend-shift_j+1] = '#'
        else:
            istart, iend = sorted((i1, i2))
            grid[istart:iend+1, j1-shift_j] = '#'

    all = np.concatenate(data, axis=0)
    shift_j = all[:, 1].min()
    m, n = all[:, 0].max() + 1, all[:, 1].max() - shift_j + 1
    grid = np.full((m, n), '.')
    src_pos = 0, 500-shift_j
    grid[src_pos] = '+'
    for indices in data:
        for start, end in zip(indices[:-1], indices[1:]):
            draw(*start, *end)

    return grid, shift_j, src_pos


example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
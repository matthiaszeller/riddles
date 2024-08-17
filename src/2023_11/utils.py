from pathlib import Path

import numpy as np

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> np.ndarray:
    return np.array([
        np.array(list(line))
        for line in data.splitlines()
    ])

from pathlib import Path

import numpy as np


def parse_data(data: str) -> np.ndarray:
    grid = np.array([np.array(list(line)) for line in data.splitlines()])
    return grid


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

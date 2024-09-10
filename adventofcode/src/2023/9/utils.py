from pathlib import Path

import numpy as np

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> np.ndarray:
    return np.array([
        list(map(int, line.strip().split()))
        for line in data.splitlines()
    ])


def solve_line(a: np.ndarray):
    diffs = [np.diff(a)]
    while not (diffs[-1] == 0.).all():
        diffs.append(np.diff(diffs[-1]))

    # traverse each level by adding the difference with previous level
    levels = diffs[:-1][::-1] + [a]
    prev_val = 0
    for level in levels:
        prev_val = level[-1] + prev_val

    return prev_val

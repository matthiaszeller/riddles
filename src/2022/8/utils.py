from pathlib import Path

import numpy as np
from pandas.io.sas.sas_constants import dataset_length


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    return np.array([list(map(int, line)) for line in data.splitlines()])


def print_grid(heights: np.ndarray, mask: np.ndarray = None):
    heights = heights.astype(str)
    if mask is not None:
        add = np.full_like(heights, '')
        add[~mask] = '\u0336'
        heights = np.char.add(heights, add)

    print('\n'.join(''.join(line) for line in heights))


example = """30373
25512
65332
33549
35390"""

example2 = """
999999999
003332223
124004451
999999999
""".strip()

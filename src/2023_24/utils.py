from pathlib import Path

import numpy as np
import sympy


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


def parse_data(data: str, dim: int) -> tuple[np.ndarray, np.ndarray]:
    def parse_line(line: str):
        p, v = line.split(' @ ')
        return list(map(int, p.split(', '))), list(map(int, v.split(', ')))

    lines = map(parse_line, data.splitlines())
    p, v = np.array(list(zip(*lines)))
    return p[:, :dim], v[:, :dim]


def norm(u: np.ndarray) -> np.ndarray:
    length = (u ** 2).sum(axis=1) ** 0.5
    return u / length.reshape(-1, 1)


def get_vect(*name: str, dim: int = 2):
    def inner(name):
        expr = ' '.join(f'{name}_{i}' for i in range(1, dim+1))
        return sympy.Matrix(sympy.symbols(expr))

    if len(name) == 1:
        return inner(name[0])
    return list(map(inner, name))


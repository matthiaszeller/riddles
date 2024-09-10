from itertools import cycle

from utils import *


def move(moves: str, nodes: dict[tuple[str, str]], src: str = 'AAA', dst: str = 'ZZZ'):
    n = 0
    current = src
    for next_move in cycle(moves):
        if current == dst:
            return n

        idx = 0 if next_move == 'L' else 1
        current = nodes[current][idx]
        n += 1


moves, nodes = parse_data(load_data())
print(move(moves, nodes))

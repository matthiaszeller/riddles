from copy import deepcopy

from utils import *


def solve(stacks, moves):
    stacks = deepcopy(stacks)

    def move(n: int, src: int, dst: int):
        to_move = stacks[src - 1][-n:]
        stacks[src - 1] = stacks[src - 1][:-n]
        stacks[dst - 1].extend(to_move)

    for mv in moves:
        move(*mv)

    return stacks


stacks, moves = parse_data(load_data())
moved = solve(stacks, moves)
sol = ''.join(s[-1] for s in moved)


from copy import deepcopy

from utils import *


def solve(stacks: list[list[str]], moves: list[tuple[int, int, int]]):
    stacks = deepcopy(stacks)

    def move(n: int, src: int, dst: int):
        if n == 0:
            return

        item = stacks[src - 1].pop()
        stacks[dst - 1].append(item)
        move(n-1, src, dst)

    for mv in moves:
        move(*mv)

    return stacks


stacks, moves = parse_data(load_data())
moved = solve(stacks, moves)
sol = ''.join([stack[-1] for stack in moved])

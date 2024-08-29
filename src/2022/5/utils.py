from pathlib import Path

import numpy as np


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def parse_stacks(stacks: str):
    lines = stacks.splitlines()
    stacks = []
    for line in lines:
        j = 0
        rest = line
        while rest:
            if len(stacks) <= j:
                stacks.append([])

            item, rest = rest[:3].strip(' []'), rest[3:]
            if item:
                stacks[j].append(item)

            rest = rest[1:]
            j += 1

    stacks = [
        stack[:-1][::-1]
        for stack in stacks
    ]

    return stacks


def parse_data(data: str):
    def parse_move(move: str):
        _, n, _, src, _, dst = move.split()
        return int(n), int(src), int(dst)

    stacks, moves = data.split('\n\n')
    stacks = parse_stacks(stacks)
    moves = list(map(parse_move, moves.splitlines()))
    return stacks, moves

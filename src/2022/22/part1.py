

from utils import *


def solve(world: np.ndarray, instr: list[int | str]):
    def move(i: int, j: int, n: int) -> tuple[int, int]:
        if n == 0:
            return i, j

        debug[i, j] = facing
        res = next_pos(i, j, facing)
        if res is None:
            return i, j

        return move(*res, n-1)

    facing = '>'
    start, next_pos = next_pos_factory(world)
    debug = world.copy()
    pos = move(*start, instr[0])
    for turn, move_n in zip(instr[1::2], instr[2::2]):
        facing = next_facing(facing, turn)
        pos = move(*pos, move_n)

    return pos, facing, debug


def compute_pwd(pos, facing):
    # don't need to remove padding, as in this riddle we start counting from 1
    i, j = pos
    facing = {'>': 0, 'v': 1, '<': 2, '^': 3}[facing]
    return 1000 * i + 4 * j + facing


world, instr = parse_data(load_data())
print_map(world)
print(instr)
pos, facing, debug = solve(world, instr)
print_map(debug)
print(compute_pwd(pos, facing))

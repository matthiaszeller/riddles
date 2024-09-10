

from utils import *


def simulate(moves: list[tuple[str, int]]):
    iH, jH, iT, jT = [0] * 4
    history: list[tuple[tuple, tuple]] = [((0, ) * 2, ) * 2]

    for direction, n in moves:
        di, dj = MOVES_MAP[direction]
        for _ in range(n):
            iH, jH = iH + di, jH + dj
            iT, jT = update_tail(iH, jH, iT, jT)
            history.append(((iH, jH), (iT, jT)))

    return history


def count_tail_positions(history: list[tuple[tuple, tuple]]) -> int:
    pos = set(t for _, t in history)
    return len(pos)


data = parse_data(example)
history = simulate(data)
print_history(history, data)
print(count_tail_positions(history))

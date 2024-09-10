

from utils import *


def simulate(moves: list[tuple[str, int]], n_knots: int = 10):
    positions = [(0, 0)] * n_knots
    history: list[list[Pos]] = [positions.copy()]

    for direction, n in moves:
        di, dj = MOVES_MAP[direction]
        for _ in range(n):
            iH, jH = positions[0]
            positions[0] = (iH + di, jH + dj)

            for k in range(1, n_knots):
                (iH, jH), (iT, jT) = positions[k-1:k+1]
                positions[k] = update_tail(iH, jH, iT, jT)

            history.append(positions.copy())

    return history


def count_tail_positions(history: list[list[Pos]]) -> int:
    pos = set(t for *_, t in history)
    return len(pos)


data = parse_data(load_data())
history = simulate(data)
#print_history(history, data)
print(count_tail_positions(history))

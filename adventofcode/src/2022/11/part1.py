import numpy as np

from utils import *


def play_round(data, divive: bool = True):
    n_inspections = [0] * len(data)
    for i, (items, operation, test_div, (dst_true, dst_false)) in enumerate(data):
        n_inspections[i] += len(items)
        for worry in items:
            worry = operation(worry)
            if divive:
                worry //= 3
            dst = dst_true if worry % test_div == 0 else dst_false
            data[dst][0].append(worry)
        # monkey inspected all its items, empty its items
        items.clear()

    return n_inspections


def play(data, rounds: int):
    n_inspections = np.zeros(len(data), dtype=int)
    for i in range(rounds):
        n = np.array(play_round(data))
        n_inspections += n

    return n_inspections


data = parse_data(load_data())
n = play(data, 20)
sol = n.copy()
sol.sort()
sol = np.prod(sol[-2:])

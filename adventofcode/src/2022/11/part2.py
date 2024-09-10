import numpy as np

from utils import *

# Problem: the numbers get insanely large, with hundreds of digits after few 100s rounds
# Trick: notice that for k > 0,
#        (a mod k*n) mod n = a mod n
# So instead, we can keep track of worried-ness modulo something
# In order for all division conditions to hold, we take product of all divisors



def play_round(data, mod):
    n_inspections = [0] * len(data)
    for i, (items, operation, test_div, (dst_true, dst_false)) in enumerate(data):
        n_inspections[i] += len(items)
        for worry in items:
            worry = operation(worry) % mod
            dst = dst_true if worry % test_div == 0 else dst_false
            data[dst][0].append(worry)
        # monkey inspected all its items, empty its items
        items.clear()

    return n_inspections


def play(data, rounds: int):
    mod = np.prod([e[2] for e in data])
    n_inspections = np.zeros(len(data), dtype=int)
    for i in range(rounds):
        n = np.array(play_round(data, mod))
        n_inspections += n

    return n_inspections


data = parse_data(load_data())
n = play(data, 10_000)
n.sort()
sol = np.prod(n[-2:])
print(sol)

from collections import deque

from utils import *


def simulate_button(modules: dict[str, Module], n: int = 1, debug: bool = False, acc=(0, 0)):
    if n == 0:
        return acc

    q: deque[tuple[str, str, Pulse]] = deque()
    q.append(('button', 'broadcaster', Pulse.low))

    n_low, n_high = acc
    while len(q) > 0:
        src, dst, pulse = q.popleft()

        # count pulses
        if pulse is Pulse.low:
            n_low += 1
        else:
            n_high += 1

        if debug:
            print(f'{src} -{pulse}-> {dst}')

        dst = modules[dst]
        response_pulse = dst.send(src, pulse)
        if response_pulse is None:
            continue

        for name in dst.dest:
            q.append((dst.name, name, response_pulse))

    if n > 1 and debug:
        print('-' * 20)
    return simulate_button(modules, n-1, debug, (n_low, n_high))


def solve(modules, n):
    n, m = simulate_button(modules, n)
    return n * m


# part 1
data = load_data()
modules = parse_data(data)
n = solve(modules, 1000)

# part 2
modules = parse_data(data)
m = 0
while modules['rx'].last_received is not Pulse.low:
    simulate_button(modules)

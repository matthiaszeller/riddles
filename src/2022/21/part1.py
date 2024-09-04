from collections import defaultdict

from utils import *


def solve(initial_src: dict[str, int], initial_wait: dict[str, tuple[Callable, str, str]]):
    src = initial_src.copy()
    wait = initial_wait.copy()
    while len(wait) > 0:
        delete_waiter = []
        for id, (op, a, b) in wait.items():
            if a in src and b in src:
                n = op(src[a], src[b])
                # this monkey isn't waiting anymore
                delete_waiter.append(id)
                src[id] = n

        for d in delete_waiter:
            del wait[d]

    return src


src, wait = parse_data(load_data())
sol = solve(src, wait)

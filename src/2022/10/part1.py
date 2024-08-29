from utils import *


def solve(data: list[tuple[int, int]]):
    X = 1
    cycle = 0
    N = 0
    values = []
    for ncycle, n in data:
        Ncycle = (20 + N * 40)
        if (cycle + ncycle) % Ncycle < ncycle:
            values.append((Ncycle, X))
            N += 1

        cycle += ncycle
        X += n

    return values


data = parse_data(data)
X = solve(data)
sol = sum([a * b for a, b in X])
print(sol)

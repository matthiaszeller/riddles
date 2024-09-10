from string import ascii_lowercase, ascii_uppercase

from utils import *


PRIORITIES = {
    a: i for i, a in enumerate(ascii_lowercase, 1)
}
PRIORITIES.update({
    A: i for i, A in enumerate(ascii_uppercase, 27)
})


def solve(data: list[tuple[str, str]]):
    res = []
    for p1, p2 in data:
        common = set(p1).intersection(p2)
        assert len(common) == 1
        common = next(iter(common))
        res.append(common)

    return res


data = parse_data(load_data())
res = solve(data)
sol = sum(PRIORITIES[c] for c in res)
print(sol)

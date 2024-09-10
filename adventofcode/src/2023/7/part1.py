

from utils import *


def solve(data: list[Hand]):
    data = sorted(data)
    scores = [
        data[i].bid * (i + 1)
        for i in range(len(data))
    ]
    return scores


if __name__ == '__main__':
    data = parse_data(example)
    data[0], data[3] = data[3], data[0]
    res = solve(data)
    print(sum(res))

    data = parse_data(load_data())
    res = solve(data)
    print(sum(res))

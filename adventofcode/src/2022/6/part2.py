from collections import Counter

from utils import *


def find_marker(stream: str, n_distinct: int = 14):
    counter = Counter(stream[:n_distinct])
    for i, c in enumerate(stream[n_distinct:], n_distinct):
        (_, n), = counter.most_common(1)
        if n == 1:
            return i - 1

        counter[c] += 1
        counter[stream[i-n_distinct]] -= 1

    return i


for e in examples:
    print(f'{find_marker(e)+1:<4} {e}')


print(find_marker(load_data()) + 1)

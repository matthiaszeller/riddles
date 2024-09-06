
from collections import Counter, deque
from utils import *


def find_marker(stream: str):
    counter = Counter(stream[:4])
    for i, c in enumerate(stream[4:], 4):
        (_, n), = counter.most_common(1)
        if n == 1:
            return i - 1

        counter[c] += 1
        counter[stream[i-4]] -= 1

    return i


for e in examples:
    print(f'{find_marker(e)+1:<4} {e}')


m = find_marker(load_data())
print(m+1)

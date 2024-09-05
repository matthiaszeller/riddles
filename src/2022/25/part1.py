

from utils import *


def solve(numbers: list[str]):
    snafu = map(snafu_to_base10, numbers)
    tot = sum(snafu)
    return base10_to_snafu(tot)


decimals = list(range(11)) + [15, 20, 2022, 12345, 314159265]

for d in decimals:
    print(f'{d:>10} {base10_to_snafu(d)}')

print()
for snafu in example.splitlines():
    print(f'{snafu:>10} {snafu_to_base10(snafu)}')

print()
print(solve(data.splitlines()))

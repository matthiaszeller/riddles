
from utils import *


def apply_map(n: int, ranges: list[tuple[int, int, int]]):
    # find range where source corresponds to n
    # by default, linear map until first source range
    rng = (0, 0, min(ranges, key=lambda rng: rng[1])[1])
    for dst, src, span in ranges:
        if src <= n <= src + span:
            rng = (dst, src, span)
            break

    dst, src, span = rng
    dist = n - src
    return dst + dist


def apply_maps(seed, chain, ranges):
    n = seed
    out = {'seed': n}
    for src_desc, dst_desc in zip(chain[:-1], chain[1:]):
        n = apply_map(n, ranges[(src_desc, dst_desc)])
        out[dst_desc] = n

    return out


def solve(seeds, chain, ranges):
    locations = [
        apply_maps(seed, chain, ranges)['location']
        for seed in seeds
    ]
    return min(locations)


seeds, chain, ranges = parse_data(example)

ns = apply_maps(seeds[0], chain, ranges)
print(solve(seeds, chain, ranges))

data = parse_data(load_data())
print(solve(*data))

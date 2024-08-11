
from utils import *


def indices_around_star(i, j):
    for ii in range(-1, 2):
        for jj in range(-1, 2):
            if ii == 0 and jj == 0:
                continue

            yield i+ii, j+jj


def get_adj_nums(grid):
    # identify numbers and their positions
    nums = find_numbers(grid)
    num_pos = [
        (num, set(zip(rows, cols)))
        for num, rows, cols in nums
    ]
    # identify stars
    mask_gear = data == '*'
    rows, cols = np.where(mask_gear)

    gear_nums = {}
    for i, j in zip(rows, cols):
        buffer = set()
        for ii, jj in indices_around_star(i, j):
            for num, idx_set in num_pos:
                if (ii, jj) in idx_set:
                    buffer.add((num, tuple(idx_set)))
        gear_nums[(i, j)] = buffer

    return gear_nums


def solve(grid):
    gear_nums = get_adj_nums(grid)
    s = 0
    for numpos in gear_nums.values():
        nums, *_ = zip(*numpos)
        if len(nums) == 2:
            s += nums[0] * nums[1]

    return s


data = parse_grid(example)
print(solve(data))
data = parse_grid(get_data())
print(solve(data))

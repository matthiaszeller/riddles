import numpy as np
from PIL.ImageChops import offset

from utils import *

# As a general consideration, we can have a single routine working for viewing on 4 sides, having
# argument axis (0 or 1) and forward (True or False).
#
# Idea 1: use np.diff to check visibility of trees, use cumsum to propagate blocking trees
#         -> problem: for [h, h-1, h+1], the invisible tree h-1 would wrongly block h+1
# Idea 2: use "cumulative max" to check max minimum visible height at each position
#         difficulty lies in cases like [h-1 h h h h-1 h+2] where in the [h h h] sequence, only the first is visible


# the following fails for 003332223 when viewed from the right

# def visible_from_side(heights: np.ndarray, axis: int, forward: bool) -> np.ndarray:
#     if not forward:
#         heights = np.flip(heights, axis=axis)
#
#     # differences of heights: zero values detect trees behind another tree of the same length
#     diff = np.diff(heights, axis=axis, prepend=-1)
#     mask_behind = diff == 0
#     # such operation would map [h-1 h h h h+1] -> [0 1 1 1 0]
#     # only the first tree behind a tree of same height would cause minimum visible height to increase by 1
#     # so we want [h-1 h h h h h+1 h+1 h-1] -> [0 1 0 0 0 0 1 0]
#     # here, detect where changes (0->1 or 1->0) occur
#     mask_first_behind = np.diff(mask_behind, axis=axis, prepend=-2) == 1
#
#     # similar to np.cumsum but here accumulate the max height
#     # those first trees behind other trees of same height cause minimum visible height to increase by 1
#     min_height = np.maximum.accumulate(heights + mask_first_behind, axis=axis)
#
#     mask = heights == min_height
#
#     if not forward:
#         mask = np.flip(mask, axis=axis)
#
#     return mask

def min_visible_height_1d(arr: np.ndarray) -> np.ndarray:
    """
    >>> min_visible_height_1d([1, 2, 2, 3])
    array([1, 2, 3, 3])
    >>> min_visible_height_1d([1, 2, 2, 2, 1, 2])
    array([1, 2, 3, 3, 3, 3])
    >>> min_visible_height_1d([0, 5, 2, 5, 6])
    array([0, 5, 6, 6, 6])
    """
    acc = [arr[0]]
    next_offset = 1
    for val in arr[1:]:
        if val > acc[-1]:
            # no need to take offset into account, since val >= acc+offset
            acc.append(val)
            next_offset = 1
        elif val == acc[-1]:
            acc.append(val + next_offset)
            # Invert offset:
            # if offset was 1, means we saw a tree of height val, and now height val remains the min visible height
            # if offset was 0, means height val if first tree seen of height val so next trees need to be higher
            next_offset = 1 - next_offset
        else:
            acc.append(acc[-1] + next_offset)
            next_offset = 0

    return np.array(acc)


def visible_from_side(heights: np.ndarray, axis: int, forward: bool) -> np.ndarray:
    if not forward:
        heights = np.flip(heights, axis=axis)

    min_visible_height = np.apply_along_axis(min_visible_height_1d, axis=axis, arr=heights)
    mask = heights == min_visible_height

    if not forward:
        mask = np.flip(mask, axis=axis)

    return mask


def solve(heights: np.ndarray) -> np.ndarray:
    return np.stack([
        visible_from_side(heights, axis, forward)
        for axis in (0, 1)
        for forward in (True, False)
    ])


if __name__ == '__main__':
    data = parse_data(load_data())
    #data = parse_data(example)
    visible = solve(data)
    print(visible.any(axis=0).sum())
    print_grid(data, visible.any(axis=0))
#
#
# subseq = '53366665342'
# for i, line in enumerate(data.astype(str)):
#     line = ''.join(line)
#     j = line.find(subseq)
#     if j >= 0:
#         break
#
# mask = np.full(data.shape, False)
# j += 5
# mask[:, j] = True
# mask[i] = True
# debug = data.astype(str).copy()
# debug[~mask] = ' '
# debug_visible = visible[0].copy()
# debug_visible[~mask] = True
# print()
# print_grid(debug, debug_visible)

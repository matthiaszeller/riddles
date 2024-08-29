from utils import *


def solve(data: list[tuple[int, int]], ncol=40, nrow=6):
    pixels = [
        [''] * ncol
        for _ in range(nrow)
    ]
    cycles = 0
    X = 1
    for ncycle, n in data:
        for _ in range(ncycle):
            # draw during cycle: check if 1 of the 3 sprite pixels is drawn
            i, j = divmod(cycles, ncol)  # i is row, j is col being drawn
            drawn_pixel_overlaps_sprite = X - 1 <= j <= X + 1
            pixels[i][j] = '#' if drawn_pixel_overlaps_sprite else '.'

            cycles += 1
        # end of cycle(s): update register
        X += n

    return pixels


data = parse_data(data)
res = solve(data)
print('\n'.join(''.join(line) for line in res))

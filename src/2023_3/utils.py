from pathlib import Path

import numpy as np


example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def get_data():
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_grid(data: str) -> np.ndarray:
    return np.array([
        np.array([c for c in line])
        for line in data.splitlines()
    ])


def find_numbers(grid: np.ndarray):
    def process_digits(digits):
        num, rows, cols = zip(*digits)
        num = int(''.join(num))
        return num, np.array(rows), np.array(cols)

    nums = []
    for i, line in enumerate(grid):
        # list of tuples (char, row, col)
        digits = []
        for j, char in enumerate(line):
            if char.isdigit():
                digits.append((char, i, j))
            elif len(digits) > 0:
                nums.append(process_digits(digits))
                digits.clear()

        # case where number extends up to right edge
        if len(digits) > 0:
            nums.append(process_digits(digits))

    return nums

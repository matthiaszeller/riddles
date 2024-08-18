from enum import Enum
from pathlib import Path

import numpy as np

example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> np.ndarray:
    return np.array([
        np.array(list(line))
        for line in data.splitlines()
    ])


class Direction(Enum):
    top = (-1, 0)
    right = (0, 1)
    left = (0, -1)
    bottom = (1, 0)


def next_directions(current_tile: str, current_direction: Direction):
    match current_tile:
        case '.':
            return [current_direction]
        case '/':
            match current_direction:
                case Direction.top:
                    return [Direction.right]
                case Direction.left:
                    return [Direction.bottom]
                case Direction.bottom:
                    return [Direction.left]
                case Direction.right:
                    return [Direction.top]
        case '\\':
            match current_direction:
                case Direction.top:
                    return [Direction.left]
                case Direction.right:
                    return [Direction.bottom]
                case Direction.bottom:
                    return [Direction.right]
                case Direction.left:
                    return [Direction.top]
        case '-':
            if current_direction == Direction.left or current_direction == Direction.right:
                return [current_direction]

            return [Direction.left, Direction.right]
        case '|':
            if current_direction == Direction.top or current_direction == Direction.bottom:
                return [current_direction]

            return [Direction.top, Direction.bottom]


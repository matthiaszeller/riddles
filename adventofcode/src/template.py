
# Standard library imports
import pathlib
import sys
from typing import TypeVar

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

# PLACEHOLDER {utils}


# @line_parser
def parse_data(input: str):
    """Parse input."""


def part1(data):
    """Solve part 1."""


def part2(data):
    """Solve part 2."""


if __name__ == '__main__':
    examples, data = load_riddle_files(__file__)
    for i, example in enumerate(examples):
        print_formatted(f'{"=" * 20} Example {i + 1}:', color='g', bold=True)
        print(example)
        example = parse_data(example)
        print_formatted(f'{"-" * 20} Parsed', color='b')
        print(example)
        print_formatted(f'{"-" * 20} Solution', color='b')
        print_formatted(f'Part 1: {part1(example)}', color='r')
        print_formatted(f'Part 2: {part2(example)}', color='r')
        print()

    # sys.exit()
    data = parse_data(data)
    print_formatted(f'{"=" * 20} Data:', color='g', bold=True)
    out1, res1 = capture_stdout(part1, data, discard=False)
    print_formatted(f'Part 1: {res1}', color='r', bold=True)
    out2, res2 = capture_stdout(part2, data, discard=False)
    print_formatted(f'Part 2: {res2}', color='r', bold=True)

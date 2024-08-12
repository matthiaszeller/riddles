

from utils import *


def calculate_points(numbers: set, winners: set) -> int:
    matches = winners.intersection(numbers)
    if len(matches) == 0:
        return 0

    return 2 ** (len(matches) - 1)


data = parse_data(get_data())

points = [
    calculate_points(*tpl) for tpl in data
]
print(sum(points))

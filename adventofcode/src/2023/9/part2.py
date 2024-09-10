

from utils import *

data = parse_data(load_data())
lines = [
    solve_line(line[::-1])
    for line in data
]
print(sum(lines))

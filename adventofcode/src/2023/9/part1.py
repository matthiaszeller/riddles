

from utils import *

data = parse_data(example)
print(sum(map(solve_line, data)))

data = parse_data(load_data())
print(sum(map(solve_line, data)))

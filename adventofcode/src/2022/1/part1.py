from utils import *


data = parse_data(load_data())
tot = list(map(sum, data))
sol = max(tot)
print(sol)

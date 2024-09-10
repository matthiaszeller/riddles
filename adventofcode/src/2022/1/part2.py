from utils import *


data = parse_data(load_data())
tot = list(map(sum, data))
tot.sort(reverse=True)
print(sum(tot[:3]))



from utils import *



print(hash_algo('HASH'))

print(sum(map(hash_algo, parse_data(example))))
print(sum(map(hash_algo, parse_data(load_data()))))

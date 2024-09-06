

from utils import *


data = parse_data(load_data())
root = build_tree(data)

avail = 70_000_000
required = 30_000_000

used = root.total_size
need_to_free = used - (avail - required)

candidates = [folder for folder in root.walk(only_dirs=True) if folder.total_size >= need_to_free]
sol = min(candidates, key=lambda e: e.total_size)

print(f'free folder {sol} of size {sol.total_size}')

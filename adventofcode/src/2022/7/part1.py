

from utils import *


data = parse_data(load_data())
root = build_tree(data)
print(root.tree())

threshold = 100_000
folders = [folder for folder in root.walk(only_dirs=True) if folder.total_size <= threshold]
sol = sum(f.total_size for f in folders)
print(sol)

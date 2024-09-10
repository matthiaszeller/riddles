

from utils import *
from part1 import *


grid = Grid.from_grid(parse_data(load_data()))
# start -> end
_, (t1, _), _, grids = solve(grid)
print('start -> goal in', t1, 'minutes')

# end -> start
_, (t2, _), _, grids = solve(grids[t1], start=grid.end, end=grid.start, initial_time=t1)
print(f'goal -> start in {t2-t1} minutes (total {t2})')

# start -> end
_, (t3, _), _, grids = solve(grids[t2], initial_time=t2)
print(f'goal -> start in {t3-t2} minutes (total {t3})')



from pathlib import Path

import numpy as np


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    return np.array(list(map(list, data.splitlines())))


example = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

example2 = """..........
.>v....v..
.......>..
.........."""

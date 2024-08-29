import argparse
from pathlib import Path

UTILS = """from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    pass

"""


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('year', type=int)
    p.add_argument('day', type=int)
    args = p.parse_args()

    root = Path(__file__).parent
    folder = root.joinpath('src', str(args.year), str(args.day))
    folder.mkdir(parents=True)

    for f in ('part1.py', 'part2.py', 'data.txt'):
        fp = folder / f
        fp.touch()

    with (folder / 'utils.py').open('w') as fh:
        fh.write(UTILS)

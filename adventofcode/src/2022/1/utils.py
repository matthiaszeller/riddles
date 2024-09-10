from pathlib import Path

from networkx import dag_longest_path


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> list[list[int]]:
    return [
        list(map(int, block.splitlines()))
        for block in data.split('\n\n')
    ]


examples = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

from pathlib import Path

example = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str):
    def parse_line(line: str) -> tuple[str, tuple[str, str]]:
        src, dst = line.split(' = ')
        return src, tuple(dst.strip('()').split(', '))

    moves, nodes = data.split('\n\n')
    nodes = dict(map(parse_line, nodes.splitlines()))
    return moves, nodes

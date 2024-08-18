from pathlib import Path


example = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


def parse_data(data: str) -> list[str]:
    return data.split(',')


def hash_step(val: int, c: str):
    val += ord(c)
    val *= 17
    val %= 256
    return val


def hash_algo(string: str):
    val = 0
    for c in string:
        val = hash_step(val, c)
    return val


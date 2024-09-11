from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


example = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

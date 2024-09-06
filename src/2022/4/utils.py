from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    return [
        tuple(map(int, line.replace('-', ',').split(',')))
        for line in data.splitlines()
    ]


example = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

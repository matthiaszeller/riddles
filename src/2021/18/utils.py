from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()

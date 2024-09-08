from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str) -> str:
    """Converts hexadecimal to binary string. Output is padded with leading zeros to have multiple of 4."""
    return bin(int(data, base=16))[2:].zfill(len(data) * 4)

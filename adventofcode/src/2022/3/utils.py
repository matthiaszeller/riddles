from pathlib import Path

def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    def parse_line(line):
        n = len(line)
        assert n % 2 == 0
        n //= 2
        return line[:n], line[n:]

    return list(map(parse_line, data.splitlines()))


example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

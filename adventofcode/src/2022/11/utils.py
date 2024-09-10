from pathlib import Path


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()
    
    
def parse_data(data: str):
    def parse_monkey(txt: str):
        lines = txt.splitlines()
        items = list(map(int, lines[1].split(': ')[1].split(',')))
        operation = lines[2].split(': ')[1].split(' = ')[1]
        operation = eval(f'lambda old: {operation}')
        test_div = int(lines[3].split()[-1])
        dst = int(lines[4].split()[-1]), int(lines[5].split()[-1])

        return items, operation, test_div, dst

    return list(map(parse_monkey, data.split('\n\n')))



example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

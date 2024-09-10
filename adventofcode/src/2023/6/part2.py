

from part1 import example, data, solve


def parse_data(data):
    l1, l2 = [
        line.split(':')[1].replace(' ', '')
        for line in data.splitlines()
    ]
    return int(l1), int(l2)


if __name__ == '__main__':
    print(solve([parse_data(example)]))
    print(solve([parse_data(data)]))

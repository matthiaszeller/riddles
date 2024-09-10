

example = """Time:      7  15   30
Distance:  9  40  200"""


data = """Time:        61     67     75     71
Distance:   430   1036   1307   1150"""


def parse_data(data):
    l1, l2 = [
        line.split(':')[1].strip().split()
        for line in data.splitlines()
    ]
    return [
        (int(a), int(b))
        for a, b in zip(l1, l2)
    ]


def find_winning_durations(duration: int, record: int):
    wins = []
    for hold_dt in range(1, duration):
        remaining_time = duration - hold_dt
        speed = hold_dt
        distance = remaining_time * speed
        if distance > record:
            wins.append((hold_dt, distance))

    return wins


def solve(data):
    n = 1
    for duration, record in data:
        wins = find_winning_durations(duration, record)
        n *= len(wins)

    return n


if __name__ == '__main__':
    print(solve(parse_data(example)))
    print(solve(parse_data(data)))

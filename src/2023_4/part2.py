from utils import *


example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


data = parse_data(example)


def process_card(i: int, counts: list, numbers: set, winners: set):
    matches = winners.intersection(numbers)
    points = len(matches)
    n = counts[i]
    for j in range(i+1, i+points+1):
        counts[j] += n


def process_cards(data):
    counts = [1] * len(data)
    for i, (numbers, winners) in enumerate(data):
        process_card(i, counts, numbers, winners)

    return counts


counts = process_cards(data)
print(sum(counts))

data = parse_data(get_data())
counts = process_cards(data)
print(sum(counts))

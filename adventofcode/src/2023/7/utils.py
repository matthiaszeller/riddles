from collections import Counter
from functools import total_ordering
from pathlib import Path


example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def load_data() -> str:
    return Path(__file__).parent.joinpath('data.txt').read_text()


@total_ordering
class Hand:

    CARD_ORDER = 'AKQJT98765432'[::-1]

    def __init__(self, cards: str, bid: int = 0):
        assert len(cards) == 5
        self.cards = cards
        self.bid = bid
        self.hand_type = self._hand_type()

    def _hand_type(self):
        counts = Counter(self.cards)
        (_, mc1), = counts.most_common(1)
        match len(counts):
            case 1:
                return 5  # five of a kind
            case 2 if mc1 == 4:
                return 4  # four of a kind
            case 2:
                return 3  # full house
            case 3 if mc1 == 3:
                return 2  # three of a kind
            case 3:
                return 1  # two pairs
            case 4:
                return 0
            case 5:
                return -1

    def __eq__(self, other: 'Hand'):
        return self.cards == other.cards

    def __lt__(self, other: 'Hand'):
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type == other.hand_type:
            for idx in range(5):
                i, j = self.CARD_ORDER.find(self.cards[idx]), self.CARD_ORDER.find(other.cards[idx])
                if i < j:
                    return True
                if i > j:
                    return False

        return False

    def __repr__(self):
        return f'Hand("{self.cards}")'


def parse_data(data: str, cls: type[Hand] = Hand):
    hands = []
    for line in data.splitlines():
        cards, bid = line.split()
        hands.append(cls(cards, int(bid)))

    return hands


def main():
    test = list(map(
        Hand, ['AAAAA', 'AA8AA', '23332', 'TTT98', '23432', 'A23A4', '23456']
    ))
    for c in test:
        print(c, c.hand_type)
    for i in range(len(test)-1):
        print(test[i] > test[i+1], end=', ')
    print()
    print(Hand('33332') > Hand('2AAAA'))


if __name__ == '__main__':
    main()

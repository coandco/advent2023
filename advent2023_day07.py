from collections import Counter
from typing import Tuple

from utils import read_data
import time

HAND_TYPES = {
    (5,): (7, "Five of a kind"),
    (1, 4): (6, "Four of a kind"),
    (2, 3): (5, "Full house"),
    (1, 1, 3): (4, "Three of a kind"),
    (1, 2, 2): (3, "Two pair"),
    (1, 1, 1, 2): (2, "One pair"),
    (1, 1, 1, 1, 1): (1, "High card")
}

CARD_STRENGTHS = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10} | {str(x): x for x in range(2, 10)}
REVISED_STRENGTHS = {k: v for k, v in CARD_STRENGTHS.items() if k != "J"} | {"J": 1}


class PartOneHand:
    raw_hand: str
    bid: int
    type: Tuple[int, str]

    def __init__(self, line: str):
        self.raw_hand, raw_bid = line.split()
        self.bid = int(raw_bid)
        self.type = self.determine_type()

    def determine_type(self):
        return HAND_TYPES[tuple(sorted(Counter(self.raw_hand).values()))]

    def card_strength(self, position: int):
        return CARD_STRENGTHS[self.raw_hand[position]]

    def __lt__(self, other: 'PartOneHand'):
        assert self.raw_hand != other.raw_hand, "Not supposed to have identical hands"
        if self.type == other.type:
            for i in range(5):
                if self.raw_hand[i] == other.raw_hand[i]:
                    continue
                return self.card_strength(i) < other.card_strength(i)

        else:
            return self.type < other.type


class PartTwoHand(PartOneHand):
    def determine_type(self):
        counts = Counter(self.raw_hand)
        num_jokers = counts.pop('J', None)
        if num_jokers:
            most_common_card, _ = counts.most_common(1)[0] if counts.most_common(1) else ('J', 0)
            counts[most_common_card] += num_jokers
        return HAND_TYPES[tuple(sorted(counts.values()))]

    def card_strength(self, position: int):
        return REVISED_STRENGTHS[self.raw_hand[position]]


def main():
    part_one_hands = sorted(PartOneHand(x) for x in read_data().splitlines())
    print(f"Part one: {sum(x.bid * (i+1) for i, x in enumerate(part_one_hands))}")
    part_two_hands = sorted(PartTwoHand(x) for x in read_data().splitlines())
    print(f"Part two: {sum(x.bid * (i+1) for i, x in enumerate(part_two_hands))}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

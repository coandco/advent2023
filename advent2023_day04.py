from utils import read_data
import time


class Card:
    part_one_value: int
    part_two_value: int

    def __init__(self, line):
        _, all_nums = line.split(": ", maxsplit=1)
        winstr, mystr = all_nums.split(" | ", maxsplit=1)
        winning_numbers = set(int(x) for x in winstr.split())
        my_numbers = set(int(x) for x in mystr.split())
        num_matches = len(winning_numbers & my_numbers)
        self.part_one_value = pow(2, num_matches-1) if num_matches else 0
        self.part_two_value = num_matches


def main():
    cards = [Card(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(x.part_one_value for x in cards)}")
    copies = {x: 1 for x in range(len(cards))}
    for i in range(len(cards)):
        for j in range(i+1, i+1+cards[i].part_two_value):
            copies[j] += copies[i]
    print(f"Part two: {sum(copies.values())}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

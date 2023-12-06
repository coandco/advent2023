from math import prod

from utils import read_data
import time
import re

DIGITS = re.compile(r'\d+')


# The value of holding a given amount will always monotonically increase, peak, and then start decreasing.
# Therefore, all we need to do is find where it passes the threshold at the start, then find where
# it passes the threshold again at the end.  Once we do that, we can assume that everything in the middle
# is over the threshold.
def ways_to_beat(race_time: int, race_distance: int) -> int:
    race_start = None
    for i in range(1, race_time):
        if i * (race_time - i) > race_distance:
            race_start = i
            break
    race_end = None
    for i in range(race_time, 0, -1):
        if i * (race_time - i) > race_distance:
            # We want to include the one we just found in the total, hence +1
            race_end = i + 1
            break
    return race_end - race_start


def main():
    raw_time, raw_distance = read_data().splitlines()
    races = list(zip((int(x) for x in DIGITS.findall(raw_time)), (int(y) for y in DIGITS.findall(raw_distance))))
    print(f"Part one: {prod(ways_to_beat(*x) for x in races)}")
    new_time = int(''.join(str(x[0]) for x in races))
    new_distance = int(''.join(str(x[1]) for x in races))
    print(f"Part two: {ways_to_beat(new_time, new_distance)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")

from aocd.exceptions import PuzzleLockedError
from aocd.models import Puzzle
from pathlib import Path
import sys

# This is a standalone script meant to be run to automatically grab my data
# for a given year/day and dump it into an automatically-named file.

YEAR_NUM = 2023

old_max_day = len(list(Path('inputs/').glob('*.txt')))
new_day = old_max_day + 1

try:
    puzzle = Puzzle(year=YEAR_NUM, day=new_day)

    file_location = Path(f'inputs/advent{YEAR_NUM}_day{new_day:02d}_input.txt')
    file_location.write_text(puzzle.input_data)
except PuzzleLockedError as e:
    print(f"Day {new_day} not available: {e}")
    sys.exit(1)


program_location = Path(f"advent{YEAR_NUM}_day{new_day:02d}.py")
blank_day = """from utils import read_data
import time


def main():
    pass


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
"""

if not program_location.exists():
    program_location.write_text(blank_day)

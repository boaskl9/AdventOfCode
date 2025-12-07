import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

def getElement(lines, row, column):
    return lines[row][column]

def getAdjacentElements(lines, row, column):
    returnList = []

    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if row == i and column == j:
                continue

            if i < 0 or j < 0:
                continue

            if i > len(lines) - 1 or j > len(lines[i]) - 1:
                continue

            returnList.append(getElement(lines, i, j))

    return returnList

def getRollCount(list):
    sum = 0

    for place in list:
        if place == '@':
            sum += 1

    return sum

def canBeReached(amount):
    return amount < 4

def eval(lines, i, j):
    return canBeReached(getRollCount(getAdjacentElements(lines, i, j)))

def solve_part1(lines):
    # Make a mutable copy of lines as we'll be modifying them
    lines = [line for line in lines]

    rollCounter = 0

    # Part 1: Only ONE iteration (single pass)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '.':
                pass  # Empty space
            else:
                if eval(lines, i, j):
                    rollCounter += 1

    return rollCounter

def solve_part2(lines):
    # Make a mutable copy of lines as we'll be modifying them
    lines = [line for line in lines]

    rollCounter = 0
    changes = 1

    # Part 2: Loop until no more changes (convergence)
    while changes > 0:
        changes = 0

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == '.':
                    pass  # Empty space
                else:
                    if eval(lines, i, j):
                        rollCounter += 1

                        before = lines[i][:j]
                        after = lines[i][j+1:]

                        lines[i] = before + '.' + after
                        changes += 1

    return rollCounter

run_day(
    day=4,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=13,  # Add expected test answer if known
    test_part2=43
)

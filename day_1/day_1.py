import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

def solve_part1(lines):
    minvalue = 0
    maxvalue = 99
    counter = 50
    passZeroCounter = 0
    landOnZeroCounter = 0

    def add(amount):
        nonlocal counter, passZeroCounter

        for i in range(amount):
            counter += 1
            if counter > maxvalue:
                counter = minvalue
                passZeroCounter += 1

    def sub(amount):
        nonlocal counter, passZeroCounter

        for i in range(amount):
            counter -= 1
            if counter == 0:
                passZeroCounter += 1
            if counter < minvalue:
                counter = maxvalue

    def rotate(amount, isPositive):
        if isPositive:
            add(amount)
        else:
            sub(amount)

    def parse(inputLine):
        direction = inputLine[0]
        amount = int(inputLine[1:])

        if direction == "R":
            rotate(amount, True)
        elif direction == "L":
            rotate(amount, False)

    for l in lines:
        parse(l)
        if counter == 0:
            landOnZeroCounter += 1

    return landOnZeroCounter

def solve_part2(lines):
    minvalue = 0
    maxvalue = 99
    counter = 50
    passZeroCounter = 0

    def add(amount):
        nonlocal counter, passZeroCounter

        for i in range(amount):
            counter += 1
            if counter > maxvalue:
                counter = minvalue
                passZeroCounter += 1

    def sub(amount):
        nonlocal counter, passZeroCounter

        for i in range(amount):
            counter -= 1
            if counter == 0:
                passZeroCounter += 1
            if counter < minvalue:
                counter = maxvalue

    def rotate(amount, isPositive):
        if isPositive:
            add(amount)
        else:
            sub(amount)

    def parse(inputLine):
        direction = inputLine[0]
        amount = int(inputLine[1:])

        if direction == "R":
            rotate(amount, True)
        elif direction == "L":
            rotate(amount, False)

    for l in lines:
        parse(l)

    return passZeroCounter

run_day(
    day=1,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=3,  # No test input available
    test_part2=6
)

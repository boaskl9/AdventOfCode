import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

def isEven(num):
    return num % 2 == 0

def checkRangePart1(start, end):
    total = 0
    for num in range(start, end + 1, 1):
        numStr = str(num)
        strLen = len(numStr)

        if isEven(strLen):
            halfLen = int(strLen / 2)

            if numStr[:halfLen] == numStr[halfLen:]:
                total += num
    return total

def checkNum(num):
    numStr = str(num)

    for subStrLen in range(1, 50):
        if len(numStr) == subStrLen:
            break

        subsections = (len(numStr) / subStrLen)

        parts = []

        if subsections == int(subsections):
            for j in range(0, int(subsections)):
                parts.append(numStr[j*subStrLen:subStrLen + j*subStrLen])

        if len(parts) == 0:
            continue

        allSame = True
        p0 = parts[0]

        for p in parts:
            if p != p0:
                allSame = False
                break

        if allSame:
            return int(num)

    return 0

def checkRangePart2(start, end):
    total = 0
    for num in range(start, end + 1, 1):
        total += checkNum(num)
    return total

def solve_part1(lines):
    splitLine = lines[0].split(',')
    runningTotal = 0

    for s in splitLine:
        ranges = s.split('-')
        runningTotal += checkRangePart1(int(ranges[0]), int(ranges[1]))

    return runningTotal

def solve_part2(lines):
    splitLine = lines[0].split(',')
    runningTotal = 0

    for s in splitLine:
        ranges = s.split('-')
        runningTotal += checkRangePart2(int(ranges[0]), int(ranges[1]))

    return runningTotal

run_day(
    day=2,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=None,  # Add expected test answer if known
    test_part2=None
)

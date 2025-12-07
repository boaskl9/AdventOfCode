import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

class Bank:
    def __init__(self, line):
        self.line = line.replace('\n', '')

    def findHighest(self):
        highest = int(self.line[0])
        highestIndex = 0

        for i in range(0, len(self.line) - 1):
            if int(self.line[i]) > highest:
                highest = int(self.line[i])
                highestIndex = i

        return highest, highestIndex

    def findPair(self, high, index):
        lineRest = self.line[index + 1:]
        restHighest = self.line[index + 1]

        for c in lineRest:
            if int(c) > int(restHighest):
                restHighest = int(c)

        return str(high) + str(restHighest)

class Bank2:
    def __init__(self, line, maxLenth):
        self.line = line.replace('\n', '')
        self.maxLenth = maxLenth

    def findHighest(self, currentJolt, startIndex):
        highest = int(self.line[startIndex])
        highestIndex = startIndex

        for i in range(startIndex, len(self.line) - (self.maxLenth - 1) + len(currentJolt)):
            if int(self.line[i]) > highest:
                highest = int(self.line[i])
                highestIndex = i

        currentJolt = currentJolt + str(highest)

        if len(currentJolt) >= self.maxLenth:
            return currentJolt
        else:
            return self.findHighest(currentJolt, highestIndex + 1)

def solve_part1(lines):
    total = 0
    for l in lines:
        b = Bank2(l, 2)
        r = b.findHighest('', 0)
        if r:
            total += int(r)
    return total

def solve_part2(lines):
    total = 0
    for l in lines:
        b = Bank2(l, 12)
        r = b.findHighest('', 0)
        if r:
            total += int(r)
    return total

run_day(
    day=3,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=357,  # Add expected test answer if known
    test_part2=3121910778619
)

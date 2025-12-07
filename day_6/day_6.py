import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

class Problem:
    def __init__(self, numbers, operator):
        self.numbers = numbers
        self.operator = operator

    def getNumbers(self):
        return self.numbers

    def getCNumbers(self):
        numLength = len(self.numbers[0])

        cNumbers = []

        for l in range(numLength):
            accStr = ""
            for n in self.numbers:
                accStr += n[l]

            cNumbers.append(accStr)

        return cNumbers

    def transformNumbers(self):
        cNumbers = self.getCNumbers()
        self.numbers = cNumbers

    def solve(self):
        total = 0
        if self.operator == '*':
            total = 1

        for num in self.numbers:
            num = num.replace(' ', '')

            if num == '':
                continue

            num = int(num)

            if self.operator == '*':
                total *= num
            else:
                total += num

        return total

def parse_input(lines):
    numLines = []

    for i in range(len(lines) - 1):
        numLines.append(lines[i])

    finalLine = lines[len(lines) - 1]

    indexList = []

    for i in range(len(finalLine)):
        c = finalLine[i]

        if c != ' ':
            indexList.append(i)

    problems = []

    for i in range(len(indexList)):
        parts = []

        if i == len(indexList) - 1:
            for numline in numLines:
                parts.append(numline[indexList[i]:])
        else:
            for numline in numLines:
                parts.append(numline[indexList[i]:indexList[i+1] - 1])

        operator = finalLine[indexList[i]]

        problem = Problem(parts, operator)

        problems.append(problem)

    return problems

def solve_part1(lines):
    problems = parse_input(lines)

    sum = 0

    for p in problems:
        sum += p.solve()

    return sum

def solve_part2(lines):
    problems = parse_input(lines)

    sum = 0

    for p in problems:
        p.transformNumbers()
        sum += p.solve()

    return sum

run_day(
    day=6,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=4277556,  # Add expected test answer if known
    test_part2=3263827
)

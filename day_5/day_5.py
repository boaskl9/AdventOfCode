import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

def checkAgainstRange(ingr, range):
    r = range.split('-')
    rStart = int(r[0])
    rEnd = int(r[1])

    ingr = int(ingr)

    return ingr >= rStart and ingr <= rEnd

def checkAgainstAllRanges(ingr, ranges):
    isFresh = False

    for r in ranges:
        if checkAgainstRange(ingr, r):
            isFresh = True
            break

    return isFresh

def execute(ranges, p):
    for i in range(len(ranges)):
        if ranges[i] == "REMOVED":
            continue

        ra = ranges[i]
        r = ra.split('-')
        rStart = int(r[0])
        rEnd = int(r[1])

        for j in range(len(ranges)):
            if i == j:
                continue

            ra2 = ranges[j]
            if ra2 == "REMOVED":
                continue

            r2 = ra2.split('-')
            rStart2 = int(r2[0])
            rEnd2 = int(r2[1])

            if rStart >= rStart2 and rEnd <= rEnd2:  # Entirely within another
                ranges[i] = "REMOVED"
                break

            elif rStart <= rStart2 and rEnd >= rEnd2:  # Will remove this one in a future iteration
                continue

            elif rStart <= rEnd2 and rEnd > rEnd2:  # goes beyond another range, eg. 3-8 goes beyond 2-5, cut to 6-8
                rStart = rEnd2 + 1  # change start to 6
                ranges[i] = str(rStart) + '-' + str(rEnd)
                if p:
                    print(f"For range {ra}: case 1, making it {rStart}-{rEnd}")

            elif rEnd >= rStart2 and rStart < rStart2:  # the end of the range overlaps, eh. 2-5 overlaps 4-6, cut to 2-3
                rEnd = rStart2 - 1
                ranges[i] = str(rStart) + '-' + str(rEnd)
                if p:
                    print(f"For range {ra}: case 2, making it {rStart}-{rEnd}")
            else:
                if p:
                    print(f"For range {ra}: case 3, making it {rStart}-{rEnd}")

def countUp(ranges, p):
    totalIds = 0

    ranges.sort()
    for r in ranges:
        if r == "REMOVED":
            if p:
                print(f"Range {r} adds none")
            continue

        r = r.split('-')
        rStart = int(r[0])
        rEnd = int(r[1])

        if p:
            print(f"Range {r} adds {rEnd - (rStart - 1)}")

        totalIds += rEnd - (rStart - 1)
    return totalIds

def solve_part1(lines):
    ranges = []
    ingredients = []
    swap = False

    for i in range(len(lines)):
        if lines[i] == '':
            swap = True
            continue

        if swap:
            ingredients.append(lines[i])
        else:
            ranges.append(lines[i])

    totalFresh = 0

    for ingr in ingredients:
        if checkAgainstAllRanges(ingr, ranges):
            totalFresh += 1

    return totalFresh

def solve_part2(lines):
    ranges = []
    swap = False

    for i in range(len(lines)):
        if lines[i] == '':
            swap = True
            continue

        if not swap:
            ranges.append(lines[i])

    execute(ranges, False)
    currentTotal = countUp(ranges, False)

    iterations = 0
    diff = True
    while diff:
        iterations += 1

        execute(ranges, False)
        newTotal = countUp(ranges, False)

        diff = newTotal != currentTotal

        currentTotal = newTotal

    return currentTotal

run_day(
    day=5,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=3,  # Add expected test answer if known
    test_part2=14
)

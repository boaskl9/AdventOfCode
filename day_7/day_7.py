import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day

def isLaserAbove(row, col, lines):
    return (lines[row - 1][col] == '|' or lines[row - 1][col] == 'S')

def insertCinStr(line, pos, char):
    lineBefore = line[:pos]
    lineAfter = line [pos + 1:]
    
    return lineBefore + char + lineAfter
    

def simulateStep(lines):    
    splits = 0
    
    for row in range(len(lines)):
        line = lines[row]
        
        for col in range(len(line)):
            char = line[col]
                        
            if row > 0: # Don't simulate the first line
                if char == '.' and isLaserAbove(row, col, lines): # Move laser down
                    lines[row] = insertCinStr(lines[row], col, '|')
                    
                elif char == '^' and isLaserAbove(row, col, lines): # Perform split
                    splits += 1
                    if col - 1 >= 0 and lines[row][col - 1] == '.':
                        lines[row] = insertCinStr(lines[row], col - 1, '|')
                        
                    if col + 1 < len(line) and lines[row][col + 1] == '.':
                        lines[row] = insertCinStr(lines[row], col + 1, '|')
    
    return lines, splits


memo = {}

def simulateQStep(lines, row, col):
    if (row, col) in memo:
        return memo[(row, col)]
                    
    char = lines[row][col]
        
    if row != len(lines) - 1: # Don't simulate the first line
        if char == '.': # Move laser down
            result = simulateQStep(lines, row + 1, col)
            
        elif char == '^': # Perform split
            leftPath = 0
            rightPath = 0

            if col - 1 >= 0:
                leftPath = simulateQStep(lines, row, col - 1)
                
            if col + 1 < len(lines[row]):
                rightPath = simulateQStep(lines, row, col + 1)
                
            result = leftPath + rightPath
        else:
            result = 0
    else: 
        result =  1 # Base case, one full path found
        
    memo[(row, col)] = result # Store pos
 
    return result   

def findStartIndex(line):
    for c in range(len(line)):
        if line[c] == 'S':
            return c
        
    print("Error, no start found!!")
    return -1

def solve_part1(lines):
    # Your solution here
    newLines, splits = simulateStep(lines)
    
    return splits

def solve_part2(lines):
    # Your solution here
    return simulateQStep(lines, 1, findStartIndex(lines[0]))

run_day(
    day=7,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=21,  # Expected test answers
    test_part2=40
)
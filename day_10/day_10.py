from cmath import sqrt
import sys
from pathlib import Path
import time
from tracemalloc import start

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day, run_test

doPrint = True

def Print(str):
    if doPrint: print(str)
    
class Machine:
    def __init__(self, line):
        elements = line.split(' ')
        self.indicatorLights = elements[0]
        self.joltage = elements[len(elements) - 1]
        self.buttons = elements[1:len(elements) - 2]    
    
def solve_part1(lines):
    machines = []
    
    for l in lines:
        machines.append(Machine(l))
        
    for m in machines:
        Print(m.buttons)
    return


def solve_part2(lines):
    
    return 



run_test(
    day=10,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=7,  # Expected test answers
    test_part2=None
)

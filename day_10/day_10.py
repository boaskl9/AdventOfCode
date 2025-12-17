from cmath import sqrt
import sys
from pathlib import Path
import time
from tracemalloc import start

from numpy import character

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day, run_test

doPrint = True

def Print(str):
    if doPrint: print(str)
    
idCounter = 0

class Button:
    def __init__(self, input):
        self.values = self.buildButton(input)
        
    def buildButton(self, input) -> list[str]:
        return input.replace('(', '').replace(')', '').split(',')
    
    def __str__(self):
        return str(self.values)
    
    def getStr(self):
        return str(self.values)
        

class Machine:
    def __init__(self, line):
        global idCounter
        self.id = idCounter
        idCounter += 1
        
        # Split input line
        elements = line.split(' ')
        
        self.indicatorLights = self.buildLights(elements[0])
        
        self.joltage = self.buildJoltage(elements[len(elements) - 1])
        
        self.buttons = self.buildButtons(elements[1:len(elements) - 2])
        
    def buildLights(self, lights) -> list[bool]:
        returnLights = []
        
        for c in lights:
            if c == '[' or c == ']':
                continue
            elif c == '.':
                returnLights.append(False)
            elif c == '#':
                returnLights.append(True)
            else:
                print(f"ERROR: Invalid char in lights: {c}")
                
        return returnLights
    
    def buildJoltage(self, jolts) -> list[str]:
        return jolts.replace('{', '').replace('}', '').split(',')
    
    def buildButtons(self, buttons) -> list[Button]:    
        returnButtons = []
        
        for b in buttons:
            returnButtons.append(Button(b))
        
        return returnButtons
    
    def printButtons(self):
        rStr = ""
        for b in self.buttons:
            rStr += b.getStr()
            
        return rStr
        
    def __str__(self) -> str:
        Print(f"Machine id: {self.id}\nlights: {self.indicatorLights}\nbuttons: {self.printButtons()}\njoltage: {self.joltage}\n")
        return ""
        
    
def solve_part1(lines):
    machines = []
    
    for l in lines:
        machines.append(Machine(l))
        
    for m in machines:
        #Print(m.buttons)
        Print(m)
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

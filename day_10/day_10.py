from cmath import sqrt
from collections import deque
import sys
from pathlib import Path
import time
from tracemalloc import start
import copy
from scipy.optimize import linprog
import numpy as np
from numpy import character

from tqdm import tqdm

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
        
    def buildButton(self, input) -> list[int]:
        tmpLst = input.replace('(', '').replace(')', '').split(',') 
        rLst = []
        for item in tmpLst:
            rLst.append(int(item))
        return rLst
    
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
        
        self.lights = self.buildLights(elements[0])
        
        self.joltage = self.buildJoltage(elements[len(elements) - 1])
        
        self.buttons = self.buildButtons(elements[1:len(elements) - 1])
        
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
        tmp = jolts.replace('{', '').replace('}', '').split(',')
        rJolts = []
        for t in tmp:
            rJolts.append(int(t))
        return rJolts
    
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
        Print(f"Machine id: {self.id}\nlights: {self.lights}\nbuttons: {self.printButtons()}\njoltage: {self.joltage}\n")
        return ""

def pressButton(lights, button):
    values = button.values
    
    for v in values:
        lights[v] = not lights[v]
        
    return lights
    
def findLeastPressesPart1(machine, maxDepth) -> int:
    correctLights = machine.lights
    buttons = machine.buttons
    
    lightsTemplate = [False] * len(correctLights)    
    #Print(f"correct lights: {correctLights}\nTemplate lights: {lightsTemplate}")
    
    allPossibilities = []
    allPossibilities.append(lightsTemplate)
    
    allPossibilities2 = []
    
    for i in range(maxDepth):
        for light in allPossibilities:
            for b in buttons:
                tmpLight = light.copy()
                newLight = pressButton(tmpLight, b)
                #input(f"button: {b}, current: {newLight}, target: {correctLights}")
                if newLight == correctLights:
                    return i + 1
                allPossibilities2.append(newLight)
        
        
        allPossibilities = allPossibilities2.copy()
        allPossibilities2.clear()
                    
                
    Print(f"ERROR: Unable to find solution with depth {maxDepth}")
    return -1

def joltDiffs(corretJoltage, counter):
    joltageDiff = []
    for i in range(len(corretJoltage)):
        joltageDiff.append((i, corretJoltage[i] - counter[i]))
        
    return joltageDiff

def findLeastPressesPart2(machine) -> int:
    try:
        import pulp
    except ImportError:
        print("Please install pulp: pip install pulp")
        return -1
    
    corretJoltage = machine.joltage
    buttons = machine.buttons
    
    # Create the problem
    prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)
    
    # Decision variables: how many times to press each button
    button_vars = []
    for i, button in enumerate(buttons):
        var = pulp.LpVariable(f"button_{i}", lowBound=0, cat='Integer')
        button_vars.append(var)
    
    # Objective: minimize total button presses
    prob += pulp.lpSum(button_vars)
    
    # Constraints: each counter must reach exactly its target
    for counter_idx in range(len(corretJoltage)):
        # Sum of all button presses that affect this counter
        counter_sum = pulp.lpSum([
            button_vars[btn_idx] 
            for btn_idx, button in enumerate(buttons) 
            if counter_idx in button.values
        ])
        prob += counter_sum == corretJoltage[counter_idx], f"counter_{counter_idx}"
    
    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))  # msg=0 suppresses solver output
    
    if prob.status == pulp.LpStatusOptimal:
        total = 0
        presses = []
        for var in button_vars:
            presses.append(int(var.varValue))
            total += int(var.varValue)
        
        # Verify
        check = [0] * len(corretJoltage)
        for btn_idx, button in enumerate(buttons):
            for v in button.values:
                check[v] += presses[btn_idx]
        
        if check == corretJoltage:
            return total
        else:
            print(f"Warning: Solution doesn't verify")
            print(f"Got: {check}")
            print(f"Expected: {corretJoltage}")
            return -1
    else:
        print(f"No optimal solution found: {pulp.LpStatus[prob.status]}")
        return -1


def solveAllMachines(machines):
    from tqdm import tqdm
    
    total = 0
    failed = 0
    for machine in tqdm(machines, desc="Processing machines"):
        result = findLeastPressesPart2(machine)
        if result == -1:
            failed += 1
            print(f"Failed on a machine!")
        else:
            total += result
    
    if failed > 0:
        print(f"\nWarning: {failed} machines failed to solve")
        return -1
    
    return total


def buildMachines(lines):
    machines = []
    for l in lines:
        machines.append(Machine(l))
    return machines

def pressButtonPart2(joltageCounter, button):
    values = button.values
    
    for v in values:
        joltageCounter[v] += 1
        
    return joltageCounter
    
def solve_part1(lines):
    machines = buildMachines(lines)
        
    sum = 0
    for m in machines:
        break # skip part 1 for now.
        sum += findLeastPressesPart1(m, 8)

    return sum

def simulateSolve(machine):
    notSolved = True
    
    buttonStr = "\n"
    for b in range(len(machine.buttons)):
        buttonStr += str(b) + ": " + machine.buttons[b].getStr() + "\n"
    
    joltageCounter = [0] * len(machine.joltage)
     
    stepCounter = 0
    while notSolved:
        stepCounter += 1
        jDiffs = joltDiffs(machine.joltage, joltageCounter)
        diffs = [pair[1] for pair in jDiffs]

        pick = input(f"\n\nCurrent joltage: {joltageCounter}\nTarget joltage:  {machine.joltage}\ndifferences:     {diffs}\nButtons available: {buttonStr}")
        
        if pick == "exit" or pick == 'q':
            quit()
        
        joltageCounter = pressButtonPart2(joltageCounter, machine.buttons[int(pick)])
        
        if joltageCounter == machine.joltage:
            notSolved = False        
    
    Print(f"Solution found in {stepCounter} steps")

def solve_part2(lines):
    global idCounter 
    idCounter = 0
    
    machines = buildMachines(lines)
    
    return solveAllMachines(machines)



run_day(
    day=10,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=7,  # Expected test answers
    test_part2=33
)

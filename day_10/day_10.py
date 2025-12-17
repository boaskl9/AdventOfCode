from cmath import sqrt
import sys
from pathlib import Path
import time
from tracemalloc import start
import copy

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
    corretJoltage = machine.joltage
    buttons = machine.buttons
    
    joltageCounters = [0] * len(corretJoltage)    
    #Print(f"correct joltage: {corretJoltage}\nTemplate joltage: {joltageCounterTemplate}")
    
    allCounters = [joltageCounters]
    allCounters2 = []
    
    maxIter = 1000
    
    stepsTaken = 0
    while stepsTaken < maxIter:
        stepsTaken += 1
        input(f"all {len(allCounters)}") # \n counters: {allCounters}
        for counter in allCounters:
            
            joltageDiff = joltDiffs(corretJoltage, counter)

            joltageDiff.sort(key=lambda j: j[1], reverse=True)
            
            candidateButtons = []
            
            indiciesToMax = []
            
            _, maxDiff = joltageDiff[0]
            
            for j in joltageDiff:
                (i, diff) = j
                if diff == maxDiff:
                    indiciesToMax.append(i)
                else:
                    break
            
            # Find buttons to press           
            for b in buttons:
                #print(b)
                for index in indiciesToMax:
                    if index in b.values:
                        # press the button to see if its valid:
                        newCounter = pressButtonPart2(counter.copy(), b)
                        newDiffs = joltDiffs(corretJoltage, newCounter)
                        wentTooFar = False
                        for _, diff in newDiffs:
                            if diff < 0:
                                wentTooFar = True
                                break
                            
                        if wentTooFar:
                            continue
                        
                        candidateButtons.append(b)
            
            # Press buttons
            for b in candidateButtons:
                newCounter = pressButtonPart2(counter.copy(), b)
                
                if newCounter not in allCounters2: 
                    allCounters2.append(newCounter)
                
        allCounters = allCounters2.copy()

        # Sort by sum in descending order and take top 100
        allCounters.sort(key=lambda c: sum(c), reverse=True)
        filtered = allCounters[:1000]
                
        allCounters = filtered         
        
        allCounters2.clear()
        
        if corretJoltage in allCounters:
            return stepsTaken 
                
            #for b in candidateButtons:
            #    print(b)
        

    return -1

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
        break
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
        pick = input(f"\n\nCurrent joltage: {joltageCounter}\nTarget joltage:  {machine.joltage}\nButtons available: {buttonStr}")
        
        joltageCounter = pressButtonPart2(joltageCounter, machine.buttons[int(pick)])
        
        if joltageCounter == machine.joltage:
            notSolved = False        
    
    Print(f"Solution found in {stepCounter} steps")

def solve_part2(lines):
    global idCounter 
    idCounter = 0
    
    machines = buildMachines(lines)
        
    sum = 0
    for m in machines:
        print(m)
        sum += findLeastPressesPart2(m)
        print("\n---------------------------------\n")

    return sum



run_day(
    day=10,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=7,  # Expected test answers
    test_part2=33
)

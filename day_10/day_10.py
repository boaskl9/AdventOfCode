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

class ChoiceList():
    def __init__(self, choices, n):
        self.choices = choices
        
    def printLst(self):
        for c in self.choices:
            for b in c:
                print(b, end=' ')
            print("")
            
    def makeChoice(self):
        for c in self.choices:
            if len(c) > 0:
                b = c[0]
                self.choices.remove(c)
                return b
        
        print("ERROR: no choices to make?")
        return -1
    
    def isEmpty(self):
        return len(self.choices) <= 0
        
    def removeButton(self, index):
        removed = False
        for c in range(len(self.choices)):
            indexToRemove = []
            for b in range(len(self.choices[c])):
                if index in self.choices[c][b].values:
                    indexToRemove.append(b)
                    removed = True

            indexToRemove.sort(reverse=True)
            for i in indexToRemove:
                self.choices[c].pop(i)
                
            if len(self.choices[c]) == 0:
                self.choices.remove(self.choices[c])
                
            if removed: break
                    

                
def findLeastPressesPart2(machine) -> int:
    corretJoltage = machine.joltage
    buttons = machine.buttons
    
    joltageCounters = [0] * len(corretJoltage)    
    
    choiceLists = []
    
    jdiffs = joltDiffs(corretJoltage, joltageCounters)
    jdiffs.sort(key=lambda v: v[1], reverse=True)
    jdiffs = jdiffs[1:] #[(0, 7), (3, 7), (1, 5), (4, 2)]
    
    for i in range(len(corretJoltage)):
       
        choicesList = []
        for no in range(corretJoltage[i]):
            buttonList = []
            
            for b in buttons:
                if i in b.values:
                    buttonList.append(b)             
                    
            choicesList.append(buttonList.copy())
            
        # after all buttons have been added to all choices, it's time to prune the choices of excess buttons.
        print(f"Now pruning choice list '{i}'")

        buttonsToRemove = [] #[(0, 7), (3, 7), (1, 5), (4, 2)]
        for j in range(len(jdiffs)):
            index, maxAmount = jdiffs[j]
            startAmount = 0
            for c in choicesList:
                for b in c:
                    if index in b.values:
                        startAmount += 1
                        continue
            removedAmount = 0
            
            
            for cI in range(len(choicesList)):
                print(f"cI: {cI}")
                c = choicesList[cI]
                foundInChoice = False
                
                if len(choicesList) - removedAmount == maxAmount or startAmount - removedAmount <= maxAmount:
                    break # we have removed enough
                
                buttonsToRemove = []  # Move this inside the cI loop
                
                for bI in range(len(c)):
                    b = c[bI]
                    if index in b.values and len(c) > 1:
                        buttonsToRemove.append(b)
                        print(f"MARK FOR REMOVE: {b}")
                        foundInChoice = True
                
                if len(buttonsToRemove) == len(c):
                    print(f"REMOVE MARKs FOR REMOVE!")
                    foundInChoice = False
                    buttonsToRemove.clear()
                    
                
                if foundInChoice:
                    removedAmount += 1
                    
                print(f"print all choices")
                for c_display in choicesList:
                    for b in c_display:
                        print(f"b: {b}", end=" ")
                    print("")
                
                # Remove buttons from THIS specific choice
                for b in buttonsToRemove:
                    print("TRY TO REMOVE", end=": ")
                    if b in c:
                        print("SUCESS")
                        c.remove(b)
                    else:
                        print("FAILURE")
                
                print(f"removed amount: {removedAmount}")

                    
        print(f"=========\n\n=========")
                        
                
        choiceList = ChoiceList(choicesList, corretJoltage[i])
        
        choiceLists.append(choiceList)
    
    maxIter = 100
    currentStep = 0
    
    currentLst = 0
    
    while currentStep < maxIter:
        currentStep += 1

        for i in range(len(choiceLists)):
            if not choiceLists[i].isEmpty():
                currentLst = i
                break
            elif i == len(choiceLists) - 1:
                return currentStep
 
        
        print(f"print all choices, and pick from '#{currentLst}'")
        for c in range(len(choiceLists)):
            print(f"#{c}")
            choiceLists[c].printLst()
            print("")
                    
        b = choiceLists[currentLst].makeChoice()
        print(f"picked button {b}")
        
        buttonValues = b.values
        
        for c in choiceLists:
            if c != choiceLists[currentLst]:
                for v in buttonValues:
                    c.removeButton(v)
            
        joltageCounters = pressButtonPart2(joltageCounters, b)
        
        print(f"joltage counter: {joltageCounters}")
        
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
    
    #simulateSolve(machines[0])
    '''sum = 0
    for m in machines:
        print(m)
        sum += findLeastPressesPart2(m)
        print("\n---------------------------------\n")'''

    return findLeastPressesPart2(machines[1]) #findLeastPressesPart2(machines[0]) + findLeastPressesPart2(machines[1]) + findLeastPressesPart2(machines[2])



run_test(
    day=10,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=7,  # Expected test answers
    test_part2=33
)

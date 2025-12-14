from cmath import sqrt
import sys
from pathlib import Path
import time
from tracemalloc import start

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day, run_test

def findHighest(lines):
    xValues, yValues = getPairs(lines)
        
    xValues.sort(reverse=True)
    yValues.sort(reverse=True)
    
    print(f" xValues[0], yValues[0]:  {xValues[0]}, {yValues[0]}")
    return xValues[0], yValues[0]


def draw2dArray(array):
    for y in array:
        for x in y:
            print(x, end="")
            
        print("")
        
        
def getPairs(lines):
    xValues = []
    yValues = []
    
    for l in lines:
        split = l.split(',')
        
        xValues.append(int(split[0]))
        yValues.append(int(split[1]))
        
    return xValues, yValues

def getPoints(lines):
    points = []
    
    for l in lines:
        split = l.split(',')
        
        points.append(Point(int(split[0]), int(split[1])))
        
    return points
    
    
def drawGrid(lines):
    gridX, gridY = findHighest(lines)
    
    xValues, yValues = getPairs(lines)
        
    drawable = []
    
    for _ in range(gridY + 2):
        dots = ['.'] * (gridX + 2)
        drawable.append(dots)
    
    for i in range(len(xValues)):
        drawable[yValues[i]][xValues[i]] = '#'
    
    draw2dArray(drawable)
    
    
def tryAll(lines):
    xValues, yValues = getPairs(lines)
    
    highestArea=0 # change me later
    bestPair = ""
    
    for p1 in range(len(xValues)):
        p1X = xValues[p1]
        p1Y = yValues[p1]
        
        for p2 in range(len(xValues)):
            p2X = xValues[p2]
            p2Y = yValues[p2]
            
            xDiff = abs(p1X - p2X) + 1   
            yDiff = abs(p1Y - p2Y) + 1
            
            area = xDiff * yDiff   

            if area > highestArea:
                highestArea = area
                bestPair = f"{p1X},{p1Y}:{p2X},{p2Y}"
    
    print(f"best pair : {bestPair} with a total area of {highestArea}")
    return highestArea

                
def solve_part1(lines):
    
    return tryAll(lines)



doPrint = False

def Print(str):
    if doPrint: print(str)

class Point:    
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        
    def getValues(self):
        return self.x, self.y

def isBetween(p1, p2, pCheck):  
    p1XisSmaller = p1.x < p2.x
    p1YisSmaller = p1.y < p2.y
    
    smallX = 0
    largeX = 0
    smallY = 0
    largeY = 0
    
    if p1XisSmaller:
        smallX = p1.x
        largeX = p2.x
    else:
        smallX = p2.x
        largeX = p1.x
    
    if p1YisSmaller:
        smallY = p1.y
        largeY = p2.y
    else:
        smallY = p2.y
        largeY = p1.y
    
    if pCheck.x > smallX and pCheck.x < largeX and pCheck.y > smallY and pCheck.y < largeY:
        Print(f"Checking point {pCheck.x},{pCheck.y} returns True")
        Print(f'''
              pCheck.x {pCheck.x}, pCheck.y {pCheck.y} 
              smallX {smallX}, smallY {smallY}
              largeX {largeX}, largeY {largeY} 
              ''')
        return True
    else:
        Print(f"Checking point {pCheck.x},{pCheck.y} returns False")
        return False
        
        
    

def checkIfLegal(p1Index, p2Index, points):
    p1 = points[p1Index]
    p2 = points[p2Index]
    
    currentPoint = p1
    
    rightTurns = 0
        
    for i in range(len(points)):

        pCheck = points[(p1Index + i + 1) % len(points)]
        nextPCheck = points[(p1Index + i + 2) % len(points)]
        Print(f"Now comparing {currentPoint.x},{currentPoint.y} to {pCheck.x},{pCheck.y}")
        
        if currentPoint.x == pCheck.x: # Moving vertically          
            Print("Moving vertically - ")     
            if currentPoint.y > pCheck.y: # Moving up
                Print("up")     
                if pCheck.x > nextPCheck.x: # Next up move LEFT!
                    Print("Next moving left!")     
                    rightTurns -= 1
                else:
                    rightTurns += 1
                    
                
            else: # Moving down
                Print("down")     
                if pCheck.x < nextPCheck.x: # Next up move RIGHT!
                    Print("Next moving right!")     
                    rightTurns -= 1
                else:
                    rightTurns += 1
            
            lowY = min (currentPoint.y, pCheck.y)
            
            for j in range(abs(currentPoint.y - pCheck.y) + 1):
                #if j % 1000 != 0: continue
                
                newPoint = Point(pCheck.x, lowY + j)
                
                if isBetween(p1, p2, newPoint):
                    return False
        
        elif currentPoint.y == pCheck.y:
            Print("Moving horizontally - ")     
            if currentPoint.x < pCheck.x: # Moving right
                Print("right")     
                if pCheck.y > nextPCheck.y: # Next up move UP!
                    Print("Next moving up!")     
                    rightTurns -= 1
                else:
                    rightTurns += 1
                    
            else: # Moving left
                Print("left")     
                if pCheck.y < nextPCheck.y: # Next up move DOWN!
                    Print("Next moving down!")     
                    rightTurns -= 1
                else:
                    rightTurns += 1
                    
            lowX = min (currentPoint.x, pCheck.x)
            
            for j in range(abs(currentPoint.x - pCheck.x) + 1):
                # if j % 1000 != 0: continue
                newPoint = Point(lowX + j, pCheck.y)
                
                if isBetween(p1, p2, newPoint):
                    return False
            
        else:
            print("ERROR: points do not line up!")
        
        currentPoint = pCheck
    
    return rightTurns > 0
        
def calculateArea(p1, p2):
    xDiff = abs(p1.x - p2.x) + 1   
    yDiff = abs(p1.y - p2.y) + 1
            
    return xDiff * yDiff   
    
def solve_part2(lines):
    
    highestArea = 0
    bestPair = (Point(-1,-1), Point(-1,-1))
    
    points = getPoints(lines)
    
    checks = 0
    
    start = time.perf_counter()
    
    for p1 in range(len(points)):
        for p2 in range(len(points)):
            if p2 <= p1: continue # Do only each pair once.
            checks+=1
            
            if checks % 1000 == 0:
                print(f"Checked {checks} pairs, and it took {time.perf_counter() - start} seconds so far")
                
            area = calculateArea(points[p1], points[p2])
            if area > highestArea:    
                if checkIfLegal(p1, p2, points):
                    highestArea = area 
        
    #print(f"best pair is {bestPair[0].x},{bestPair[0].y} and {bestPair[1].x},{bestPair[1].y} with an area of {highestArea}")
        
        
    return highestArea


    

run_day(
    day=9,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=50,  # Expected test answers
    test_part2=24
)


# Too low: 110477124 
#        : 110477124
import re
import time
from xmlrpc.client import MAXINT


def checkAgainstAllRanges(ingr, ranges):
    isFresh = False
    
    for r in ranges:
        if checkAgainstRange(ingr, r):
            isFresh = True
            break
        
    return isFresh
        

def checkAgainstRange(ingr, range):
    r = range.split('-')
    rStart = int(r[0])
    rEnd = int(r[1])
    
    ingr = int(ingr)
    
    return ingr >= rStart and ingr <= rEnd

def execute(p):
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
            
            
            if rStart >= rStart2 and rEnd <= rEnd2: # Entirely within another
                ranges[i] = "REMOVED"
                break
            
            elif rStart <= rStart2 and rEnd >= rEnd2: # Will remove this one in a future iteration
                continue
            
            elif rStart <= rEnd2 and rEnd > rEnd2: # goes beyond another range, eg. 3-8 goes beyond 2-5, cut to 6-8
                rStart = rEnd2 + 1 # change start to 6
                ranges[i] = str(rStart) + '-' + str(rEnd) 
                if p: print(f"For range {ra}: case 1, making it {rStart}-{rEnd}")
                
            elif rEnd >= rStart2 and rStart < rStart2: # the end of the range overlaps, eh. 2-5 overlaps 4-6, cut to 2-3
                rEnd = rStart2 - 1
                ranges[i] = str(rStart) + '-' + str(rEnd)
                if p: print(f"For range {ra}: case 2, making it {rStart}-{rEnd}")
            else:
                if p: print(f"For range {ra}: case 3, making it {rStart}-{rEnd}")


def countUp(p):
    totalIds = 0
    
    ranges.sort()
    for r in ranges:
        if r == "REMOVED":
            if p: print(f"Range {r} adds none")
            continue
            
        r = r.split('-')
        rStart = int(r[0])
        rEnd = int(r[1])
        
        if p: print(f"Range {r} adds {rEnd - (rStart - 1)}")
        
        totalIds += rEnd - (rStart - 1)
    return totalIds

with open("day_5/input.txt") as f:
    lines = f.read().splitlines()
    
    start = time.perf_counter()


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
            
    #print(f"Ranges are: {ranges}\nIngredeients are: {ingredients}")
    
    totalFresh = 0
    
    for ingr in ingredients:
        if checkAgainstAllRanges(ingr, ranges):
            totalFresh += 1
        
    end = time.perf_counter()
    
    print(f"Part 1 execution time: {end - start:.6f} seconds")
            
    print(f"Total amount of fresh ingredients: {totalFresh}")
    
    # ============ PART 2 ===============
    
    start = time.perf_counter()
    
    execute(False)
    currentTotal = countUp(False) 
    
    iterations = 0
    diff = True
    while diff:
        iterations += 1
        
        execute(False)
        newTotal = countUp(False) 
        
        diff = newTotal != currentTotal
        
        currentTotal = newTotal
    
    end = time.perf_counter()
    
    print(f"Part 2 execution time: {end - start:.6f} seconds")

        
    
    print(f"Total amount of fresh ids after {iterations} runs:  {currentTotal}")
    
        
        
    '''
    #print(f"for range {rStart} to {rEnd}, a total of {rEnd - (rStart - 1)} are added")
    
    if rEnd < prevHigh:
        print(f"for range {rStart} to {rEnd} with a prevhigh of {prevHigh}, None are added")
        continue
    
    totalIds += rEnd - max((rStart - 1), prevHigh)
    
    print(f"for range {rStart} to {rEnd} with a prevhigh of {prevHigh}, a total of {rEnd - max((rStart - 1), prevHigh)} are added")

    
    prevHigh = rEnd
    '''
        
        
        
            
            
'''
3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''
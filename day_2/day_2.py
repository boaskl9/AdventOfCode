import time

f = open("day_2/day_2_input.txt")

splitLine = f.readline().split(',')

runningTotalPart1 = 0
runningTotalPart2 = 0

# =============== PART 1 Start ===============
def isEven(num):
    return num % 2 == 0

def checkRangePart1(start, end):
    global runningTotalPart1
        
    for num in range(start, end + 1, 1):
        numStr = str(num)       # Current number as a string
        strLen = len(numStr)    # Lenth of that string
        
        if isEven(strLen):        
            halfLen = int(strLen / 2)
                    
            if numStr[:halfLen] == numStr[halfLen:]:
                runningTotalPart1 += num  # Found an invalid ID
# =============== PART 1 End =================
  
# =============== PART 2 Start ===============
def checkNum(num):
    global runningTotalPart2
    
    numStr = str(num)
    
    for subStrLen in range(1, 50):
        if len(numStr) == subStrLen:
            break
        
        subsections = (len(numStr) / subStrLen) 
        
        parts = []
        
        if subsections == int(subsections):
            for j in range(0, int(subsections)):
                parts.append(numStr[j*subStrLen:subStrLen + j*subStrLen])
        
        if len(parts) == 0:
            continue
        
        allSame = True
        
        p0 = parts[0]
        
        for p in parts:
            if p != p0:
                allSame = False
                break
            
        if allSame:
          runningTotalPart2 += int(num) # Found an invalid ID
          break
            
def checkRangePart2(start, end):    
    for num in range(start, end + 1, 1):
        checkNum(num)            
# =============== PART 2 End =================
                
# Execute part 1 
startPart1 = time.perf_counter()
for s in splitLine:
    ranges = s.split('-')
    checkRangePart1(int(ranges[0]),int(ranges[1]))

endPart1 = time.perf_counter()
print(f"Part 1 result: {runningTotalPart1} - Execution time: {endPart1 - startPart1:.6f} seconds")

# Execute part 2
startPart2 = time.perf_counter()
for s in splitLine:
    ranges = s.split('-')
    checkRangePart2(int(ranges[0]),int(ranges[1]))

endPart2 = time.perf_counter()
print(f"Part 2 result: {runningTotalPart2} - Execution time: {endPart2 - startPart2:.6f} seconds")
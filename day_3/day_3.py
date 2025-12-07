import time

f = open("day_3/input.txt")

lines = f.readlines()
runningTotalPart1 = 0
runningTotalPart1b = 0
runningTotalPart2 = 0

class Bank:
    def __init__(self, line):
        self.line = line.replace('\n', '')
    
    def findHighest(self):
        
        highest = int(self.line[0])
        highestIndex = 0
        
        for i in range(0, len(self.line) - 1):
            if int(self.line[i]) > highest:
                highest = int(self.line[i])
                highestIndex = i
                
        return highest, highestIndex
    
    def findPair(self, high, index):
        lineRest = self.line[index + 1:]
        restHighest = self.line[index + 1]
        
        for c in lineRest:
            if int(c) > int(restHighest):
                restHighest = int(c)
                
        return str(high) + str(restHighest)

class Bank2:
    def __init__(self, line, maxLenth):
        self.line = line.replace('\n', '')
        self.maxLenth = maxLenth
    
    def findHighest(self, currentJolt, startIndex):        
        highest = int(self.line[startIndex])
        highestIndex = startIndex

        for i in range(startIndex, len(self.line) - (self.maxLenth - 1) + len(currentJolt)):
            if int(self.line[i]) > highest:
                highest = int(self.line[i])
                highestIndex = i
                
        currentJolt = currentJolt + str(highest)
        
        if len(currentJolt) >= self.maxLenth:
            #print(f"Current jolt: {currentJolt}")
            return currentJolt
        else: 
            return self.findHighest(currentJolt, highestIndex + 1)
        
def run_part(label, func):
    start = time.perf_counter()
    result = func()
    end = time.perf_counter()

    right_padding = ('{:-<25}'.format(result))
    print(f"{label}: {right_padding}- Execution time: {end - start:.6f} seconds")

    return result

def part1(lines):
    total = 0
    for l in lines:
        b = Bank(l)
        high, index = b.findHighest()
        total += int(b.findPair(high, index))
    return total

def part1b(lines):
    total = 0
    for l in lines:
        b = Bank2(l, 2)
        r = b.findHighest('', 0)
        if r:
            total += int(r)
    return total

def part2(lines):
    total = 0
    for l in lines:
        b = Bank2(l, 12)
        r = b.findHighest('', 0)
        if r:
            total += int(r)
    return total

f = open("day_3/input.txt")
lines = f.readlines()

run_part("Part 1  result", lambda: part1(lines))
run_part("Part 1b result", lambda: part1b(lines))
run_part("Part 2  result", lambda: part2(lines))

'''
startPart1 = time.perf_counter()

for l in lines:
    # ===== PART 1 =====
    b = Bank(l)
    
    high, index = b.findHighest()

    result = b.findPair(high, index)
    
    runningTotalPart1 += int(result)

endPart1 = time.perf_counter()

right_padding = ('{:-<25}'.format(runningTotalPart1))
print(f"Part 1 result: {right_padding}- Execution time: {endPart1 - startPart1:.6f} seconds")


startPart1b = time.perf_counter()

for l in lines:
    # ===== PART 1b=====
    b = Bank2(l, 2)
    
    result = b.findHighest('', 0)
        
    if result is None:
        print("Dont do this to me")
        continue
    
    runningTotalPart1b += int(result)

endPart1b = time.perf_counter()

right_padding = ('{:-<25}'.format(runningTotalPart1b))

print(f"Part 1bresult: {right_padding}- Execution time: {endPart1b - startPart1b:.6f} seconds")

startPart2 = time.perf_counter()

for l in lines:
    # ===== PART 2 =====
    b = Bank2(l, 12)
    
    result = b.findHighest('', 0)
        
    if result is None:
        print("Dont do this to me")
        continue
    
    runningTotalPart2 += int(result)

endPart2 = time.perf_counter()

right_padding = ('{:-<25}'.format(runningTotalPart2))


print(f"Part 2 result: {right_padding}- Execution time: {endPart2 - startPart2:.6f} seconds")

'''
import time


class Problem:
    def __init__(self, numbers, operator):
        self.numbers = numbers
        self.operator = operator
        
    def getNumbers(self):
        return self.numbers
    
    def getCNumbers(self):
        
        numLength = len(self.numbers[0])
        
        cNumbers = []
        
        for l in range(numLength):
            accStr = ""
            for n in self.numbers:
                accStr += n[l]
                
            cNumbers.append(accStr)
        
        return cNumbers
    
    def transformNumbers(self):
        cNumbers = self.getCNumbers()
        
        self.numbers = cNumbers
        
    def solve(self):
        total = 0
        if self.operator == '*':
            total = 1
            
        for num in self.numbers:
            num = num.replace(' ', '')
            
            if num == '':
                continue
            
            num = int(num)
            
            if self.operator == '*':
                total *= num
            else:
                total += num
                
        return total


with open("day_6/input.txt") as f:
    lines = f.read().splitlines()
    
    numLines = []
    
    start = time.perf_counter()
    
    for i in range(len(lines) - 1):
        numLines.append(lines[i])
    
    finalLine = lines[len(lines) - 1]
    
    indexList = []
    
    for i in range(len(finalLine)):
        c = finalLine[i]
        
        if c != ' ':
            indexList.append(i)

    problems = []
    
    for i in range(len(indexList)):
        parts = []
        
        if i == len(indexList) - 1:
            for numline in numLines:
                parts.append(numline[indexList[i]:])
        else:
            for numline in numLines:
                parts.append(numline[indexList[i]:indexList[i+1] - 1])
            
        operator = finalLine[indexList[i]]
        
        problem = Problem(parts, operator)
        
        problems.append(problem)
    
    end = time.perf_counter()
                    
                    
    p0 = problems[0]
    p3 = problems[3]
    
    print(f"p0 numbers: {p0.getCNumbers()}")
    print(f"p3 numbers: {p3.getCNumbers()}")
    
    
    sum = 0
    
    for p in problems:
        sum += p.solve()
        
    print(f"Part 1: Final total sum: {sum}, expected result: 4277556. difference: {4277556 - sum}")
    
    start = time.perf_counter()

    sum = 0
    
    for p in problems:
        p.transformNumbers()
        sum += p.solve()
        
    end = time.perf_counter()
    
    print(f"Part 2 execution time: {end - start:.6f} seconds")
    
    print(f"Part 2: Final total sum: {sum}, expected result: 3263827. difference: {3263827 - sum}")

        
        
        

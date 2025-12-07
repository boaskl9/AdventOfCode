def isLaserAbove(row, col, lines):
    return (lines[row - 1][col] == '|' or lines[row - 1][col] == 'S')

def insertCinStr(line, pos, char):
    lineBefore = line[:pos]
    lineAfter = line [pos + 1:]
    
    return lineBefore + char + lineAfter
    

def simulateStep(lines):
    
    lines = lines
    
    splits = 0
    
    for row in range(len(lines)):
        line = lines[row]
        
        for col in range(len(line)):
            char = line[col]
                        
            if row > 0: # Don't simulate the first line
                if char == '.' and isLaserAbove(row, col, lines): # Move laser down
                    lines[row] = insertCinStr(lines[row], col, '|')
                    
                elif char == '^' and isLaserAbove(row, col, lines): # Perform split
                    splits += 1
                    if col - 1 >= 0 and lines[row][col - 1] == '.':
                        lines[row] = insertCinStr(lines[row], col - 1, '|')
                        
                    if col + 1 < len(line) and lines[row][col + 1] == '.':
                        lines[row] = insertCinStr(lines[row], col + 1, '|')
    
    return lines, splits

memo = {}

def simulateQStep(lines, row, col, splitsAcc):
    if (row, col) in memo:
        return memo[(row, col)]
    
    lines = lines
    
    splits = splitsAcc
        
    line = lines[row]
    
    char = line[col]
    
    #print(f'''Current line: {line}, row: {row}, col: {col}''')
    
    if row != len(lines) - 1: # Don't simulate the first line
        if char == '.': # Move laser down
            result = simulateQStep(lines, row + 1, col, splits)
            
        elif char == '^': # Perform split
            
            leftPath = 0
            rightPath = 0

            if col - 1 >= 0:
                leftPath = simulateQStep(lines, row, col - 1, splits)
                
            if col + 1 < len(line):
                rightPath = simulateQStep(lines, row, col + 1, splits)
                
            result = leftPath + rightPath
        else:
            result = 0
    else: 
        result =  1 # Base case, one full path found
        
    memo[(row, col)] = result # Store pos
 
    return result          
    
def findS(line):
    
    for c in range(len(line)):
        if line[c] == 'S':
            return c
        
    print("Error, no start found!!")
    return -1
        
def printGraphic(lines):
    for l in lines:
        print(l)
            
            
            

with open("day_7/input.txt") as f:
    lines = f.read().splitlines()
        
    #printGraphic(lines)
    
    #print("")

    
    #newLines, splits = simulateStep(lines)
    
    #printGraphic(newLines)
    #print(f"Part 1: Total amount of splits: {splits}")
    
    
    
    totalPaths = simulateQStep(lines, 1, findS(lines[0]), 0)
    
    print(f"Part 2: Total amount of paths: {totalPaths}")
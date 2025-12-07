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
                        
            if row > 0:
                if char == '.' and isLaserAbove(row, col, lines):
                    print("Case 1")
                    lines[row] = insertCinStr(lines[row], col, '|')
                elif char == '^' and isLaserAbove(row, col, lines):
                    splits += 1
                    if col - 1 >= 0 and lines[row][col - 1] == '.':
                        print("Case 2")
                        lines[row] = insertCinStr(lines[row], col - 1, '|')
                    if col + 1 < len(line) and lines[row][col + 1] == '.':
                        print("Case 3")
                        lines[row] = insertCinStr(lines[row], col + 1, '|')
    
    return lines, splits
                        
        
def printGraphic(lines):
    for l in lines:
        print(l)
            
            
            

with open("day_7/input.txt") as f:
    lines = f.read().splitlines()
        
    printGraphic(lines)
    
    print("")

    
    newLines, splits = simulateStep(lines)
    
    printGraphic(newLines)
    print(f"Total amount of splits: {splits}")
    
    
    



'''
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''
#read input 
#find @ 
#Cheak nabours ??? verdi 
#if true mark as X and add to roleconter 

row_1 = ".@."
row_2 = "@@@"
row_3 = ".@@"

example_list = [row_1, row_2, row_3]

def getElemet(row, column):
    return lines[row][column]

def getAdjecentElements(row, column):
    returnList = []
    
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if row == i and column == j:
                continue
            
            if i < 0 or j < 0:
                continue
            
            if i > len(lines) - 1 or j > len(lines[i]) - 1:
                continue
            
            returnList.append(getElemet(i, j))

    return returnList
            
def getRollCount(list):
    sum = 0
    
    for place in list:
        if place == '@':
            sum += 1
            
    return sum

def canBeReached(amount):
    return amount < 4
        
def eval(i, j):
    return canBeReached(getRollCount(getAdjecentElements(i, j)))

rollCounter = 0

with open("day_4/day_4_input.txt") as f:
    lines = f.read().splitlines()
    
    #lines = example_list
    
    
    
    changes = 1
    
    while changes > 0:
        changes = 0

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == '.':
                    print(".", end="")
                else:
                    if eval(i, j):
                        rollCounter += 1
                        print("X", end="")
                        
                        before = lines[i][:j]
                        after = lines[i][j+1:]
                        
                        lines[i] = before + '.' + after
                        changes += 1
                        
                    else:
                        print("@", end="")
                    
            print("")
    
print(f"Part 1, total amount of Paper Rolls which can be accessed by forklifts: {rollCounter}")

'''
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.


..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
'''
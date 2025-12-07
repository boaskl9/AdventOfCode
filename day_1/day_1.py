import time

start = time.perf_counter()

# ----- your code here -----

f = open("day_1_input.txt")


lines=f.readlines()

minvalue = 0
maxvalue = 99

counter = 50 
passZeroCounter = 0 
landOnZeroCounter = 0

def add(amount):
    global counter
    global passZeroCounter
    
    for i in range(amount):
        counter += 1

        if counter > maxvalue:
            counter = minvalue
            passZeroCounter += 1
            #print("Increased Pass Zero Counter!")
            
def sub(amount):
    global counter
    global passZeroCounter

    for i in range(amount):
        counter -= 1

        if counter == 0:
            passZeroCounter += 1
            #print("Increased Pass Zero Counter!")
        
        if counter < minvalue:
            counter = maxvalue

def rotate(amount,isPositive):
    if isPositive:
      add(amount)
    else:
      sub(amount)

def parse(inputLine):
    direction = inputLine[0] 
    amount = int(inputLine[1:]) 

    if direction == "R" : 
        rotate(amount,True)
    elif direction == "L" :
        rotate(amount,False)
    else: print ("Not Valid")

for l in lines:
    #print("Counter currently at: " + str(counter))
    #print("current rotation: " +  l)
    #input("press enter") #uncomment to be able to go step by step
    parse(l)

    if counter == 0:
        landOnZeroCounter += 1

print ("Day 1 part 1: " + str(landOnZeroCounter))
print ("Day 1 part 2: " + str(passZeroCounter))


end = time.perf_counter()

print(f"Execution time: {end - start:.6f} seconds")
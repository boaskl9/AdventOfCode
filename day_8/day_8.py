from cmath import sqrt
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day, run_test

id_counter = 0

class Circuit:
    def __init__(self, point):
        global id_counter
        self.id = id_counter
        id_counter+= 1
        self.points = []
        self.points.append(point)
        
    def getId(self):
        return self.id
        
    def add(self, point):
        #print("Tring to add: ", end="")
        #print(point, end=" ")
        oldCir = point.getCir()
        #print(f"which is currently in {oldCir.getId()} with len {len(oldCir.getPoints())}")

        
        for p in  oldCir.getPoints():
            #print("---------")
            self.points.append(p)
            p.setCir(self)
        
        oldCir.clear()
    

    def clear(self):
        self.points = []
        
    def remove(self, point):
        self.points.remove(point)
        
    def getLen(self):
        return len(self.points)

    def getPoints(self):
        return self.points
        
    def printLen(self):
        print(f"Circuit has {self.getLen()} points")

class Point:    
    def __init__(self, x, y, z, cir=None):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.cir = cir
        
    def getCir(self):
        return self.cir
    
    def setCir(self, cir):
        self.cir = cir
        
    def getValues(self):
        return self.x, self.y, self.z
    
    def printPoint(self):
        print(f"Point has x: {self.x}, y: {self.y}, z: {self.z}")
        
    def __str__(self):
        return f"{self.x},{self.y},{self.z}"


def distance(pointA, pointB):
    aX, aY, aZ = pointA.getValues()
    bX, bY, bZ = pointB.getValues()
    
    return (pow((aX - bX), 2) + pow((aY - bY), 2) + pow((aZ - bZ), 2))

def findShortest(points):
    distances = []
    
    for i in range(len(points)):
        p0 = points[i]
        
        for j in range(len(points)):
            if j <= i:
                continue
            
            p1 = points[j]
            
            d = (distance(p0, p1), p0, p1)
            
            distances.append(d)
    
    distances.sort(key=lambda d: d[0])
                     
    return distances

def lineToPoint(line):
    coordinates = line.split(',')
    return Point(coordinates[0], coordinates[1], coordinates[2])

def solve_part1(lines):
    circuits = []
    points = []
    for l in lines:
        p = lineToPoint(l)
        c = Circuit(p)
        p.setCir(c)
        circuits.append(c)
        points.append(p)
                
    dists = findShortest(points)
        
    connectionsMade = 0
    
    connectionsToMake = 0
    if len(lines) == 20:
        connectionsToMake = 10
    else:
        connectionsToMake = 1000
    
    while connectionsMade < connectionsToMake:
        (_, p0, p1) = dists.pop(0)
        
        if p0.getCir() != p1.getCir():
            p0.getCir().add(p1)
            #print(f"circuit {p0.getCir().getId()} now has {len(p0.getCir().getPoints())}")
        connectionsMade +=1

    circuits.sort(key=lambda d: d.getLen(), reverse=True)
        
    print(f"{circuits[0].getLen()} * {circuits[1].getLen()} * {circuits[2].getLen()}")
    
    return circuits[0].getLen() * circuits[1].getLen() * circuits[2].getLen()

def solve_part2(lines):
    circuits = []
    points = []
    for l in lines:
        p = lineToPoint(l)
        c = Circuit(p)
        p.setCir(c)
        circuits.append(c)
        points.append(p)
                
    dists = findShortest(points)
        
    connectionsMade = 0
    
    lastp0 = Point(0,0,0)    
    lastp1 = Point(0,0,0)
        
    while connectionsMade < len(lines) - 1:
        (_, p0, p1) = dists.pop(0)
        
        if p0.getCir() != p1.getCir():
            p0.getCir().add(p1)
            #print(f"circuit {p0.getCir().getId()} now has {len(p0.getCir().getPoints())}")
            connectionsMade +=1
            lastp0 = p0
            lastp1 = p1
            
    
    xp0, _, _ = lastp0.getValues()
    xp1, _, _ = lastp1.getValues()


    circuits.sort(key=lambda d: d.getLen(), reverse=True)
        
    print(f"{xp0} * {xp1}")
    
    return xp0 * xp1

run_day(
    day=8,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=40,  # Expected test answers
    test_part2=25272
)
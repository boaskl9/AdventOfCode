from cmath import sqrt
import sys
from pathlib import Path
import time
from tracemalloc import start
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aoc_helper import run_day, run_test
    
class Device():
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
        
    def __str__(self):
        return f"Device '{self.name}' has outputs {self.outputs}"

def buildDevices(lines):
    devices = []
    for l in lines:
        elements = l.split(' ')
        newDevice = Device(elements[0].replace(':', ''), elements[1:])
        devices.append(newDevice)
    return devices

def buildDictionary(devices):
    dictionary = {}
    
    for d in devices:
        dictionary[d.name] = d
        
    return dictionary

devices = {}
memo = {}

def findPaths(dFrom, dTo) -> int:    
    global memo
    
    sum = 0
    for o in dFrom.outputs:
        if o == dTo:
            sum += 1
            continue
        
        if o in memo:
            sum += memo[o]
        else:
            oDevice = devices[o]
            sum += findPaths(oDevice, dTo) # Take all paths
        
    memo[dFrom.name] = sum
    return sum

def freshFindPaths(dFrom, dTo):
    global memo
    memo.clear()
    r = findPaths(dFrom, dTo)
    return r
    
def solve_part1(lines):
    global devices
    devices = buildDictionary(buildDevices(lines))
    
    r = freshFindPaths(devices["you"], "out")
    
    return r

def solve_part2(lines):
    if len(lines) < 20:
        lines = ["svr: aaa bbb","aaa: fft","fft: ccc","bbb: tty","tty: ccc","ccc: ddd eee","ddd: hub","hub: fff","eee: dac","dac: fff","fff: ggg hhh","ggg: out","hhh: out"]

    global devices
    devices = buildDictionary(buildDevices(lines))
    devices["out"] = Device("out", [])

    fftFirst = freshFindPaths(devices["svr"], "fft") * freshFindPaths(devices["fft"], "dac") * freshFindPaths(devices["dac"], "out")
    dacFirst = freshFindPaths(devices["svr"], "dac") * freshFindPaths(devices["dac"], "fft") * freshFindPaths(devices["fft"], "out")
    
    return fftFirst + dacFirst

run_day(
    day=11,
    part1_solver=solve_part1,
    part2_solver=solve_part2,
    test_part1=5,  # Expected test answers
    test_part2=2
)
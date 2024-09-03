from Coast import*
from Salmon import*
from Bear import*
from Boat import*
import os

COAST_WIDTH = 160
COAST_HEIGHT = 80
NUM_SALMON = 50
NUM_BOATS = 6
NUM_BEARS = 10
MONITOR_INTERVAL = 1000

# The driver application for the simulation.  Adds the salmon, boats,
# and bears.  Calls runSim
def entryMethod():
    coast = Coast(COAST_WIDTH, COAST_HEIGHT)
    coast.draw()

    addSalmon(coast, NUM_SALMON)
    addBoats(coast, NUM_BOATS)
    addBears(coast, NUM_BEARS)
    runSim(coast)

# The while loops continues until the number of salmon is
# less than zero
def runSim(coast):
    try:
        cycleCounter = 1
        while coast.numLivingSalmon > 0:
            coast.liveLife()
            surveyPopulation(coast, cycleCounter)
            coast.introduceVirus()
            cycleCounter += 1
        coast.displayResults()
        coast.freezeCoast()
    except BaseException as ex:
        print(ex)

def addSalmon(coast, numSalmon):
    initSalmonRangeX = int(coast.maxX / 8)
    for i in range(numSalmon):
        salmon = Salmon()
        x = random.randrange(initSalmonRangeX)
        y = random.randrange(coast.maxY)
        while not coast.emptyLocation(x, y):
            x = random.randrange(initSalmonRangeX)
            y = random.randrange(coast.maxY)
        coast.addThing(salmon, x, y)
    coast.numStartSalmon = numSalmon
    coast.numLivingSalmon = numSalmon


def addBoats(coast, numBoats):
    boatRangeY = coast.maxX/2 + random.randrange(int(coast.maxX/5))
    for i in range(numBoats):
        newBoat = Boat()
        x = boatRangeY
        y = random.randrange(coast.maxY)
        while not coast.emptyLocation(x, y):
            x = boatRangeY
            y = random.randrange(coast.maxY)
        coast.addThing(newBoat, x, y)
    coast.numBoats = numBoats


def addBears(coast, numBears):
    bearRangeX = int(coast.maxX/1.5 + random.randrange(coast.maxX) / 3)
    for i in range(numBears):
        newBear = Bear()
        x = bearRangeX
        y = random.randrange(coast.maxY)
        while not coast.emptyLocation(x, y):
            x = bearRangeX
            y = random.randrange(coast.maxY)
        coast.addThing(newBear, x, y)
    coast.numBears = numBears
    coast.numAliveBears = numBears

# At constant interval, calls the method to monitor the salmon population health
def surveyPopulation(coast, cycleCounter):
    if cycleCounter % MONITOR_INTERVAL == 0:
        coast.monitorSalmonPopulation()

entryMethod()


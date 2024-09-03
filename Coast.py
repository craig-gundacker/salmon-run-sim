import turtle
import random
import os
from Salmon import*
from Boat import*
from Bear import*

# The setting for the simulation
class Coast:
    def __init__(self, mx, my):
        self._maxX = mx
        self.maxY = my
        self.thingList = []
        self.grid = []

        self.numBears = 0
        self.numAliveBears = 0
        self.numCubs = 0
        self.numStartSalmon = 0
        self.numLivingSalmon = 0
        self.numBoats = 0
        self.numSpawnSalmon = 0
        self.PROB_INFECTION = .001
        self.VIRUS_MORTALITY_RATE = .3
        self.REMOVE_BOAT_THRESHOLD = .6
        self.TARGET_SPAWN_RATE = .3
        self.CUB_SURVIVAL_RATE = .4
        self.ADULT_SURVIVAL_RATE = .9

        for aRow in range(self.maxY):
            row = []
            for aCol in range(self.maxX * 2):
                row.append(None)
            self.grid.append(row)

        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.screen = turtle.Screen()
        self.screen.setworldcoordinates(0, 0, (self.maxX - 1), (self.maxY - 1))
        workingDirectory = os.getcwd()
        self.screen.addshape(os.path.join(workingDirectory, 'imgs', 'bear.gif'))
        self.screen.addshape(os.path.join(workingDirectory, 'imgs', 'boat.gif'))
        self.screen.addshape(os.path.join(workingDirectory, 'imgs', 'salmon.gif'))
        self.pen.hideturtle()

    # Draws the coast
    def draw(self):
        #Draw border
        self.pen._tracer(0)
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.pendown()
        self.pen.forward(self.maxX - 1)
        self.pen.left(90)
        self.pen.forward(self.maxY - 1)
        self.pen.left(90)
        self.pen.forward(self.maxX - 1)
        self.pen.left(90)
        self.pen.forward(self.maxY - 1)
        self.pen.left(90)

        #Draw vertical and horizontal grid lines
        for i in range(self.maxY - 1):
            self.pen.forward(self.maxX - 1)
            self.pen.backward(self.maxX - 1)
            self.pen.left(90)
            self.pen.forward(1)
            self.pen.right(90)
        self.pen.forward(1)
        self.pen.right(90)
        for i in range(self.maxX - 2):
            self.pen.forward(self.maxY - 1)
            self.pen.backward(self.maxY - 1)
            self.pen.left(90)
            self.pen.forward(1)
            self.pen.right(90)
        self.pen._tracer(1)

    def freezeCoast(self):
        self.screen.exitonclick()

    # Adds salmon, boat, or bear
    def addThing(self, thing, x, y):
        x = int (x)
        y = int (y)
        thing.setX(x)
        thing.setY(y)
        self.grid[y][x] = thing
        thing.setInCoast(self)
        self.thingList.append(thing)
        thing.appear()

    # Removes salmon, boat, or bear.  Checks the type of thing
    # and decrements the counter
    def delThing(self, aThing):
        if self.thingList is not []:
            aThing.hide()
            self.grid[aThing.getY()][aThing.getX()] = None
            self.thingList.remove(aThing)
            if isinstance(aThing, Salmon):
                self.decSalmon()
            elif isinstance(aThing, Bear):
                self.decBears()
            elif isinstance(aThing, Boat):
                self.decBoats()

    # Moves thing on grid.  Sets new position and removes reference
    # to thing from old position
    def moveThing(self, oldX, oldY, newX, newY):
        self.grid[newY][newX] = self.grid[oldY][oldX]
        self.grid[oldY][oldX] = None

    @property
    def maxX(self):
        return self._maxX

    @property
    def maxY(self):
        return self._maxY

    @maxX.setter
    def maxX(self, value):
        self._maxX = value

    @maxY.setter
    def maxY(self, value):
        self._maxY = value

    # Checks if list of things is not empty.  Chooses random thing and calls
    # the liveLife method of that thing
    def liveLife(self):
        if self.thingList is not []:
            aThingNumber = random.randrange(len(self.thingList))
            randomThing = self.thingList[aThingNumber]
            randomThing.liveLife()

    # Removes boat if salmon population is too low
    def monitorSalmonPopulation(self):
        if self.removeBoatRequired:
            boatRemoved = False
            if self.numBoats > 0:
                index = 0
                while boatRemoved is False:
                    if index < len(self.thingList):
                        thing = self.thingList[index]
                        if isinstance(thing, Boat):
                            self.delThing(thing)
                            boatRemoved = True
                            self.decBoats()
                        index += 1
                    else:
                        boatRemoved = True

    # Checks if a boat removal is necessary
    def removeBoatRequired(self):
        return self.numLivingSalmon / self.numStartSalmon < self.REMOVE_BOAT_THRESHOLD

    # Introduces a salmon virus into the population.  If a random number is less than
    # the probablity of infection, the number of salmon likely to die is determined.
    # The while loop removes that number of salmon without duplicating deaths.  Finally,
    # the health of the overall population is surveyed
    def introduceVirus(self):
        if self.numLivingSalmon > 2 and random.random() < self.PROB_INFECTION:
            print("Virus Spreading")
            numSalmonThatWillDie = self.numLivingSalmon * self.VIRUS_MORTALITY_RATE
            numSalmonDied = 0
            deadFishIndex = []
            while numSalmonDied < numSalmonThatWillDie:
                aThingIndex = random.randrange(len(self.thingList))
                if aThingIndex not in deadFishIndex:
                    deadFishIndex.append(aThingIndex)
                    thing = self.thingList[aThingIndex]
                    if isinstance(thing, Salmon):
                        thing.hide()
                        self.grid[thing.getY()][thing.getX()] = None
                        self.thingList.remove(thing)
                        self.decSalmon()
                        numSalmonDied += 1
            self.monitorSalmonPopulation()
            
    def emptyLocation(self, x, y):
        x = int (x)
        y = int (y)
        if self.grid[y][x] is None:
            return True
        else:
            return False

    def peekLocation(self, x, y):
        return self.grid[y][x]

    def decBears(self):
        self.numAliveBears -= 1
        print("Bear Died")

    def decSalmon(self):
        self.numLivingSalmon -= 1
        print("Salmon Died")

    def decBoats(self):
        self.numBoats -= 1
        print("Boat Removed")

    def getNumBears(self):
        return self.numBears

    def getNumStartSalmon(self):
        return self.numStartSalmon

    def getNumLivingSalmon(self):
        return self.numLivingSalmon

    def getNumBoats(self):
        return self.numBoats

    def displayResults(self):
        print("\nNumber of fish at start of run: " + str(self.numStartSalmon))
        print("Number of fish spawned during run: " + str(self.numSpawnSalmon))
        print("Number of surviving bears: " + str(self.numBears))
        print("Expected bear cubs: " + str(self.numCubs))
        print(self.isHarvestSustainable())
        print(self.isBearPopHealthy())

    # Returns a string representing whether or not the harvest is sustainable
    def isHarvestSustainable(self):
        reproduceRateActual = self.numSpawnSalmon / self.numStartSalmon
        if reproduceRateActual >= self.TARGET_SPAWN_RATE:
            return "Sustainable harvest"
        else:
            return "Unsustainable harvest"

    def isBearPopHealthy(self):
        numSurviveCubs = self.numCubs * self.CUB_SURVIVAL_RATE
        numSurviveAdults = self.numAliveBears * self.ADULT_SURVIVAL_RATE
        numSurviveTotal = numSurviveCubs + numSurviveAdults
        print("Number of surviving bear cubs: " + str(numSurviveCubs))
        print("Number of surviving adult bears: " + str(numSurviveAdults))
        if numSurviveTotal < self.numBears:
            return "Bear Population Decreasing"
        elif numSurviveTotal == self.numBears:
            return "Bear Population Remaining Steady"
        else:
            return "Bear Population Increasing"

import turtle
import random
import os
from Salmon import*

# Represents a bear in the simulation
class Bear:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.up()
        workingDirectory = os.getcwd()
        self.turtle.shape(os.path.join(workingDirectory, 'imgs', 'bear.gif'))
        self.turtle.shapesize(.1, .1, .1)
        #self.turtle.turtlesize(.5, .5, .5)
        self.turtle.color("brown")

        self.xPos = 0
        self.yPos = 0
        self.coast = None
        self.leftBearLimit = 0

        self.starveTicker = 0
        self.breedTicker = 0
        self.bred = False
        #Eligible moves a bear can make in a single cycle
        self.moveCoords = [(-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
                           (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                           (-2, 0), (-1, 0),         (1, 0), (2, 0),
                           (-2,-1), (-1,-1), (0,-1), (1,-1), (2,-1),
                           (-2,-2), (-1,-2), (0,-2), (1,-2), (2,-2)]
        self.probCatch = .6 #Probability a bear will catch salmon
        self.breedThreshold = 1 #The number required before a bear can successfully breed
        self.starveThreshold = 30 #The number at which a bear starves

    def setX(self, newX):
        self.xPos = newX

    def setY(self, newY):
        self.yPos = newY

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos

    def setInCoast(self, aWorld):
        self.coast = aWorld
        self.leftBearLimit = int(self.coast.maxX / 1.5)

    def appear(self):
        self.turtle.goto(self.xPos, self.yPos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newX, newY):
        self.coast.moveThing(self.xPos, self.yPos, newX, newY)
        self.xPos = newX
        self.yPos = newY
        self.turtle.goto(self.xPos, self.yPos)

    # Calls the functions of a bear(eat, breed, move)
    def liveLife(self):
        self.tryToEat()
        if not self.bred and self.breedTicker >= self.breedThreshold:
            self.tryToBreed()
        if self.starveTicker > self.starveThreshold:
            self.coast.delThing(self)
        else:
            self.tryToMove()

    # Appends adjacent salmon to array.  If array is greater than 0, calls pounce method,
    # otherwise increments the bears starve ticker
    def tryToEat(self):
        adjSalmon = []
        for coord in self.moveCoords:
            newX = self.xPos + coord[0]
            newY = self.yPos + coord[1]
            if self.inTerritory(newX, newY):
                if isinstance(self.coast.peekLocation(newX, newY), Salmon):
                    adjSalmon.append(self.coast.peekLocation(newX, newY))

        if len(adjSalmon) > 0:
            self.pounce(adjSalmon)
        else:
            self.starveTicker += 1

    # Picks a random salmon from array.  If random number is less than or equal
    # to the probability of a catch, then salmon is removed, bear moves, the
    # bear starve ticker is reset and the breed ticker is incremented
    def pounce(self, adjSalmon):
        salmon = adjSalmon[random.randrange(len(adjSalmon))]
        preyX = salmon.getX()
        preyY = salmon.getY()

        randNum = random.random()
        if randNum <= self.probCatch:
            self.coast.delThing(salmon)
            self.move(preyX, preyY)
            self.starveTicker = 0
            self.breedTicker += 1
        else:
            self.starveTicker += 1

    # Determines if bear is in its territory
    def inTerritory(self, newX, newY):
        return self.leftBearLimit <= newX < self.coast.maxX and 0 <= newY < self.coast.maxY

    #If bear is successful in breeding, the bear can produce either 1 or 2 offspring
    def tryToBreed(self):
        indexMove = random.randrange(len(self.moveCoords))
        coord = self.moveCoords[indexMove]
        nextX = self.xPos + coord[0]
        nextY = self.yPos + coord[1]
        while not(self.inTerritory(nextX, nextY)):
            indexMove = random.randrange(len(self.moveCoords))
            coord = self.moveCoords[indexMove]
            nextX = self.xPos + coord[0]
            nextY = self.yPos + coord[1]#

        if self.coast.emptyLocation(nextX, nextY):
            numOffspring = random.randrange(3)
            for i in range(numOffspring + 1):
                self.coast.numCubs += 1
            self.bred = True

    #Finds an eligible location to move.  If the location has a salmon, the
    #bear tries to eat
    def tryToMove(self):
        indexMove = random.randrange(len(self.moveCoords))
        coord = self.moveCoords[indexMove]
        nextX = self.xPos + coord[0]
        nextY = self.yPos + coord[1]
        while not self.inTerritory(nextX, nextY):
            indexMove = random.randrange(len(self.moveCoords))
            coord = self.moveCoords[indexMove]
            nextX = self.xPos + coord[0]
            nextY = self.yPos + coord[1]

        if self.coast.emptyLocation(nextX, nextY):
            self.move(nextX, nextY)
        elif isinstance(self.coast.peekLocation(nextX, nextY), Salmon):
            self.tryToEat()



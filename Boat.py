import turtle
import random
from Salmon import*

class Boat:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.up()
        #self.turtle.shape('square')
        self.turtle.turtlesize(1, 1, 1)
        self.turtle.color("red")

        self.xPos = 0
        self.yPos = 0
        self.coast = None
        self.leftBoatLimit = 0
        self.rightBoatLimit = 0
        self.bankruptTicker = 0
        self.bankruptThreshold = 10
        #Grid locations, relative to the boat, that the boat's net can reach
        self.netCoords = [(-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3),
                          (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2),
                          (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
                          (-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
                          (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
                          (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2),
                          (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3)]
        #Grid locations, relative to the boat, that the boat can move
        self.moveCoords = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1,-1), (0,-1), (1,-1)]
        self.probCatch = .75 #Probability that boat will catch a salmon if salmon is in range of net

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
        self.leftBoatLimit = int(self.coast.maxX / 3)
        self.rightBoatLimit = int(self.coast.maxX / 1.5)

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

    #Calls boat functions(fish, move)
    def liveLife(self):
        self.tryToFish()
        if self.bankruptTicker > self.bankruptThreshold:
            self.coast.delThing(self)
        else:
            self.tryToMove()

    #Casts the net
    def tryToFish(self):
        adjSalmon = []
        for coord in self.netCoords:
            newX = self.xPos + coord[0]
            newY = self.yPos + coord[1]
            if self.inLegalWaters(newX, newY):
                if isinstance(self.coast.peekLocation(newX, newY), Salmon):
                    if random.random() < self.probCatch:
                        adjSalmon.append(self.coast.peekLocation(newX, newY))
                        salmon = self.coast.peekLocation(newX, newY)
                        self.coast.delThing(salmon)

        if len(adjSalmon) > 0:
            #randomFish = adjSalmon[random.randrange(len(adjSalmon))]
            #fishX = randomFish.getX()
            #fishY = randomFish.getY()
            #self.move(fishX, fishY)
            self.bankruptTicker = 0
        else:
            self.bankruptTicker += 1

    #Recursively calls tryToMove until an eligible location is found
    def tryToMove(self):
        indexMove = random.randrange(len(self.moveCoords))
        coord = self.moveCoords[indexMove]
        nextX = self.xPos + coord[0]
        nextY = self.yPos + coord[1]
        while not self.inLegalWaters(nextX, nextY):
            indexMove = random.randrange(len(self.moveCoords))
            coord = self.moveCoords[indexMove]
            nextX = self.xPos + coord[0]
            nextY = self.yPos + coord[1]

        if self.coast.emptyLocation(nextX, nextY):
            self.move(nextX, nextY)
        else:
            self.tryToMove()

    #Returns true if boat is in eligible water, else returns false
    def inLegalWaters(self, nextX, nextY):
        return self.leftBoatLimit <= nextX < self.rightBoatLimit and 0 <= nextY < self.coast.maxY

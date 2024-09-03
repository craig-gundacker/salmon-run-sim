import turtle
import random
import os
from Coast import*

class Salmon:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.up()
        workingDirectory = os.getcwd()
        self.turtle.shape(os.path.join(workingDirectory, 'imgs', 'salmon.gif'))
        self.turtle.shapesize(.1, .1, .1)
        self.turtle.turtlesize(.5, .5, .5)
        self.turtle.color("blue")

        self.xPos = 0
        self.yPos = 0
        self.moveDistX = 10
        self.moveDistY = 2
        self.moveCoords = [(0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]
        self.Coast = None

        self.breedTicker = 0

    def setX(self, newX):
        self.xPos = newX

    def setY(self, newY):
        self.yPos = newY

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos

    def setInCoast(self, aCoast):
        self.Coast = aCoast

    def appear(self):
        self.turtle.goto(self.xPos, self.yPos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newX, newY):
        self.Coast.moveThing(self.xPos, self.yPos, newX, newY)
        self.xPos = newX
        self.yPos = newY
        self.turtle.goto(self.xPos, self.yPos)

    def liveLife(self):
        self.tryToMove()

    #Moves each salmon.  If salmon has not reached end of screen (i.e, spawning
    #grounds), the salmon moves in a semi-random direction across screen.
    #Otherwise, salmon has reached spawning grounds and is deleted
    def tryToMove(self):
        moved = False
        while moved is False:
            indexMove = random.randrange(len(self.moveCoords))
            coord = self.moveCoords[indexMove]
            nextX = self.xPos + (coord[0] * self.moveDistX)
            nextY = self.yPos + (coord[1] * self.moveDistY)
            if self.xPos + self.moveDistX < self.Coast.maxX:
                if 0 <= nextY < self.Coast.maxY:
                    if self.Coast.emptyLocation(nextX, nextY):
                        self.move(nextX, nextY)
                        moved = True
            else:
                self.move(self.Coast.maxX - 1, self.yPos)
                self.Coast.numSpawnSalmon += 1
                self.Coast.delThing(self)
                moved = True

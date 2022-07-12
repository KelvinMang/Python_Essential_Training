import os
import time
from termcolor import colored
import math 


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]


    def hitsWall(self, point):
        if round(point[0]) < 0 or round(point[0]) >= self._x:
            return "vert_wall"
        elif round(point[1]) < 0 or round(point[1]) >= self._y:
            return "hori_wall"
        else:
            return "normal"

    def getReflection(self, point):
        return [-1 if self.hitsWall(point) == "vert_wall" else 1, -1 if self.hitsWall(point) == "hori_wall" else 1]

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]

        self.direction = [0, 1]

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]

    def up(self):
        self.direction = [0, -1]
        self.forward()

    def down(self):
        self.direction = [0, 1]
        self.forward()

    def right(self):
        self.direction = [1, 0]
        self.forward()

    def left(self):
        self.direction = [-1, 0]
        self.forward()
    
    def bounce(self, pos):
        reflection = self.canvas.getReflection(pos)
        self.direction = [self.direction[0] * reflection[0], self.direction[1] * reflection[1]]
        
    def forward(self,distance):
        for i in range(distance):
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            if self.canvas.hitsWall(pos) == "vert_wall" or "hori_wall":
                self.bounce(pos)
                pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            self.draw(pos)
            
    def drawSquare(self, size):
        for i in range(size):
            self.right()
        for i in range(size):
            self.down()
        for i in range(size):
            self.left()
        for i in range(size):
            self.up()

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)
    
    def drawX(self, function):
        for x in range(self.canvas._x):
            pos = [x,function(x)]
            if pos[1] and self.canvas.hitsWall(pos)=='normal':
                self.draw(pos)
        
    
    def drawaxis(self):
        for x in range(self.canvas._x):
            pos = [x,self.canvas._y/2]
            if self.canvas.hitsWall(pos)=='normal':
                self.draw(pos)

            
        for y in range(self.canvas._y):
            pos = [0,y]
            if self.canvas.hitsWall(pos)=='normal':
                self.draw(pos)



def sine(x):
    return 5*math.sin(x/4)+10

def cosine(x):
    return 10*math.cos(x/2)+10


canvas = Canvas(30, 30)
scribe = TerminalScribe(canvas)
scribe.drawaxis()
scribe.drawX(cosine)

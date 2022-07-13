import os
import time
from termcolor import colored
import math 
import random

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

class CanvasAxis(Canvas):
    def formatAxisNumber(self,number):
        if number % 5 != 0 : 
            return '  '
        if number < 10 :
            return ' ' + str(number)
        return str(number)

    def print(self):
        self.clear()
        for y in range(self._y):
            print(self.formatAxisNumber(y) + ' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas, color='red', mark='*', trail='.', pos=(0, 0), framerate=.05, direction=[0, 1]):
        self.canvas = canvas
        self.trail = trail
        self.mark = mark
        self.framerate = framerate
        self.pos = pos
        self.color = color
        self.direction = direction

    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]
    
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
            
    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, self.color))
        self.canvas.print()
        time.sleep(self.framerate)

class Robotplot(TerminalScribe):
    def up(self, distance = 1):
        self.direction = [0, -1]
        self.forward(distance)

    def down(self, distance = 1):
        self.direction = [0, 1]
        self.forward(distance)

    def right(self, distance = 1):
        self.direction = [1, 0]
        self.forward(distance)

    def left(self,distance = 1):
        self.direction = [-1, 0]
        self.forward(distance)

    def drawSquare(self, size):
        for i in range(size):
            self.right()
        for i in range(size):
            self.down()
        for i in range(size):
            self.left()
        for i in range(size):
            self.up()

class plotfunctions(TerminalScribe):
    def drawX(self, function):
        for x in range(self.canvas._x):
            pos = [x,function(x)]
            if pos[1] and self.canvas.hitsWall(pos)=='normal':
                self.draw(pos)

    def drawaxis(self):
        for x in range(self.canvas._x):
            pos = [x,0]
            if self.canvas.hitsWall(pos)=='normal':
                self.draw(pos)
                
        for y in range(self.canvas._y):
            pos = [0,y]
            if self.canvas.hitsWall(pos)=='normal':
                self.draw(pos)

class mathsfunction:
    def sine(x):
        return 5*math.sin(x/4)+10

    def cosine(x):
        return 10*math.cos(x/2)+10
    
    def tan(x):
        return 10*math.tan(x/4)+10

class RandomWalkScribe(TerminalScribe):
    def __init__(self, canvas, degrees=135, **kwargs):
        super().__init__(canvas, **kwargs)
        self.degrees = degrees
    
    def randomizeDegreeOrientation(self):
        self.degrees = random.randint(self.degrees-10, self.degrees+10)
        self.setDegrees(self.degrees)
    
    def bounce(self, pos):
        reflection = self.canvas.getReflection(pos)
        if reflection[0] == -1:
            self.degrees = 360 - self.degrees
        if reflection[1] == -1:
            self.degrees = 180 - self.degrees
        self.direction = [self.direction[0] * reflection[0], self.direction[1] * reflection[1]]

    def forward(self, distance):
        for i in range(distance):
            self.randomizeDegreeOrientation()
            super().forward(1)


canvas = CanvasAxis(30,30)
Robotscribe = Robotplot(canvas, color = 'red')
Robotscribe.drawSquare(10)

Plotscribe = plotfunctions(canvas, color = 'blue')
Plotscribe.drawaxis()
Plotscribe.drawX(mathsfunction.sine)

randomScribe = RandomWalkScribe(canvas, color='green', pos=(0, 0))
randomScribe.forward(1000)

import os
import time
import math
from termcolor import colored

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

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
        self.framerate = 0.1
        #This set the plot starts in the middle of the canvas, so we can plot the direction in 360 degrees
        self.pos = [canvas._x/2,canvas._y/2]  
        self.direction = [0,1]
    
    def setposition(self,position):
        self.pos = position

    def setdegree(self,angle):
        radians = ((angle)/180)*math.pi
        self.direction = [math.sin(radians),-math.cos(radians)]
    
    def forward(self):
        pos = [self.pos[0]+ self.direction[0], self.pos[1]+self.direction[1]]
        if not self.canvas.hitsWall(pos):
         self.draw(pos)

    def up(self):
        self.direction = [0,-1]
        self.forward()

    def down(self):
        self.direction = [0,1]
        self.forward()

    def right(self):
        self.direction = [1,0]
        self.forward()

    def left(self):
        self.direction = [-1,0]
        self.forward()

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)
    
    def drawsquare(self,size):
        for num in range(size-1):
            self.right()
        for num in range(size-1):
            self.down()
        for num in range(size-1):
            self.left()
        for num in range(size-1):
            self.up()

canvas = Canvas(30, 30)

scribe = [
        {"starting_pos" :[15,15] , "direction" : 30, "movement" :[
            {"function" : "forward", "duration" : 5},
            {"function" : "left", "duration" : 10},
            {"function" : "right", "duration" : 6},
            ]},
        {"starting_pos" : [10,10], "direction": 135, "movement" :[
            {"function" : "down", "duration" : 10},
            {"function" : "forward", "duration" : 5},
            {"function" : "left" , "duration": 7},
            ]}
]

for scribeData in scribe:
    #New Scribe Object
    scribeData["scribe"] = TerminalScribe(canvas)
    scribeData["scribe"].setposition(scribeData["starting_pos"])
    scribeData["scribe"].setdegree(scribeData["direction"])

    # Flatten instructions:
    # Convert "{'left': 10}" to ['left', 'left', 'left'...]
    scribeData['instructions_flat'] = []

    # is still within the scribeData in scribe for loop
    for instruction in scribeData['movement']:
    #We make movement["function"] as a list as well so we will do join two list every loop 
        scribeData['instructions_flat'] = scribeData['instructions_flat'] + [instruction['function']]*instruction['duration']
    
    print(scribeData['instructions_flat'])

maxInstructionLength = max([len(scribeData['instructions_flat']) for scribeData in scribe])

for i in range(maxInstructionLength):
    for scribeData in scribe:
        if i < len(scribeData['instructions_flat']):
            if scribeData['instructions_flat'][i] == 'forward':
                scribeData['scribe'].forward()
            elif scribeData['instructions_flat'][i] == 'drawSquare':
                scribeData['scribe'].drawSquare()
            elif scribeData['instructions_flat'][i] == 'up':
                scribeData['scribe'].up()
            elif scribeData['instructions_flat'][i] == 'down':
                scribeData['scribe'].down()
            elif scribeData['instructions_flat'][i] == 'left':
                scribeData['scribe'].left()
            elif scribeData['instructions_flat'][i] == 'right':
                scribeData['scribe'].right()





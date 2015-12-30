from ..logger import *
from ..config import numberBarWidth

class Cursor:

    buffer = None
    y, x = 0, 0

    def __init__(self):
        self.y = 0
        self.x = numberBarWidth

    def guardRange(self):
        if self.y < 0:
            self.y = 0
        elif self.y > len(self.buffer) - 1:
            self.y = len(self.buffer) - 1
        line = self.buffer[self.y]
        if self.x < numberBarWidth:
            self.x = numberBarWidth
        elif self.x > len(line) + numberBarWidth:
            self.x = len(line) + numberBarWidth

    def position(self, y = None, x = None):
        if y == None and x == None:
            return (self.y, self.x)
        if y != None: self.y = y
        if x != None: self.x = x
        self.guardRange()

    def moveVertical(self, offset):
        y = self.y + offset
        height = self.buffer.length()
        if y < 0: y = 0
        if y > height: y = height
        self.y = y
        self.guardRange()

    def moveHorizontal(self, offset):
        y = self.y
        width = self.buffer[y].length()
        x = self.x + offset
        if x < 0: x = 0
        if x > width: x = width
        self.x = x
        self.guardRange()

    def trackHorizontalInsert(self, x, length):
        if x <= self.x: self.x += length

    def trackHorizontalDelete(self, x, length):
        if x < self.x:
            self.x -= length
            if self.x < x: self.x = x

    def trackVerticalInsert(self, y, length):
        if y <= self.y: self.y += length

    def trackVerticalDelete(self, y, length):
        if y < self.y:
            self.y -= length
            if self.y < y: self.y = y


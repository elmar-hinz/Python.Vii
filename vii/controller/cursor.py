from ..logger import *
from ..signals import *

class Cursor:

    buffer = None
    y, x = 0, 0

    def __init__(self, buffer):
        self.buffer = buffer
        slot("verticalInsert", self)
        slot("horizontalInsert", self)
        slot("verticalDelete", self)
        slot("horizontalDelete", self)

    def receive(self, signal, sender, *args):
        if sender == self.buffer:
            if signal == "verticalInsert":
                self.trackVerticalInsert(*args)
            if signal == "horizontalInsert":
                self.trackHorizontalInsert(*args)
            if signal == "verticalDelete":
                self.trackVerticalDelete(*args)
            if signal == "horizontalDelete":
                self.trackHorizontalDelete(*args)

    def position(self, y = None, x = None):
        if y == None and x == None:
            return (self.y, self.x)
        if y != None: self.y = y
        if x != None: self.x = x
        self.update()

    def guardRange(self):
        if self.y < 0:
            self.y = 0
        elif self.y > self.buffer.length() - 1:
            self.y = self.buffer.length() - 1
        line = self.buffer.getLine(self.y)
        if self.x < 0:
            self.x = 0
        elif self.x > len(line):
            self.x = len(line)

    def moveVertical(self, offset):
        y = self.y + offset
        height = self.buffer.length()
        if y < 0: y = 0
        if y >= height: y = height - 1 # cursor can't stay behind last line
        self.y = y
        self.update()

    def moveHorizontal(self, offset):
        y = self.y
        width = len(self.buffer.getLine(y))
        x = self.x + offset
        if x < 0: x = 0
        if x > width: x = width # cursor can stay behind last char by ONE
        self.x = x
        self.update()

    def trackHorizontalInsert(self, x, length):
        if x <= self.x: self.x += length
        self.update()

    def trackHorizontalDelete(self, x, length):
        if x < self.x:
            self.x -= length
            if self.x < x: self.x = x
        self.update()

    def trackVerticalInsert(self, y, length):
        if y <= self.y: self.y += length
        self.update()

    def trackVerticalDelete(self, y, length):
        if y < self.y:
            self.y -= length
            if self.y < y: self.y = y
        self.update()

    def update(self):
        self.guardRange()
        signal("cursorMoved", self)


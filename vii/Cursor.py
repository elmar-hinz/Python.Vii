from .Logger import *
from .Signals import *
from .BufferRanges import BufferRanges

class Cursor:

    def __init__(self):
        self.buffer = None
        self.ranges = None
        self.x = 0
        self.y = 0
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
        elif self.y > self.buffer.countOfLines() - 1:
            self.y = self.buffer.countOfLines() - 1
        length = self.buffer.lengthOfLine(self.y)
        if self.x < 0:
            self.x = 0
        elif self.x > length:
            self.x = length

    def moveVertical(self, offset):
        y = self.y + offset
        height = self.buffer.countOfLines()
        if y < 0: y = 0
        if y >= height: y = height - 1 # cursor can't stay behind last line
        self.y = y
        self.update()

    def moveHorizontal(self, offset):
        y = self.y
        width = self.buffer.lengthOfLine(y)
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

    """ Buffer range movements """

    def appendInLine(self):
        self.position(*self.ranges.appendInLine())

    def beginningOfBuffer(self):
        self.position(*self.ranges.beginningOfBuffer())

    def beginningOfLine(self):
        self.position(*self.ranges.beginningOfLine())

    def down(self, factor = 1):
        self.position(*self.ranges.down(factor))

    def endOfBuffer(self):
        self.position(*self.ranges.endOfBuffer())

    def endOfLine(self):
        self.position(*self.ranges.endOfLine())

    def left(self, factor = 1):
        self.position(*self.ranges.left(factor))

    def right(self, factor = 1):
        self.position(*self.ranges.right(factor))

    def up(self, factor = 1):
        self.position(*self.ranges.up(factor))


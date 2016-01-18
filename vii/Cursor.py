from .Logger import *
from .Signals import *
from .BufferRanges import BufferRanges

class Cursor:
    """
    Observes the buffer.
    Tracks inserting and deleting.

    Keeps the cursor inside the range of buffer
    if movements go out of bounds.
    Cursor can stay 1 behing length of line
    to enable appending.
    Position adjustments should happen in BufferRanges,
    while only exceptions are thrown here.
    """

    def __init__(self):
        self.buffer = None
        self.ranges = None
        self.x = 1
        self.y = 1
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
        if self.y < 1: self.y = 1
        elif self.y > self.buffer.countOfLines() :
            self.y = self.buffer.countOfLines()
        length = self.buffer.lengthOfLine(self.y)
        if self.x < 1: self.x = 1
        elif self.x > length + 1: self.x = length + 1

    def trackHorizontalInsert(self, x, length):
        if x <= self.x: self.x += length
        self.update()

    def trackHorizontalDelete(self, x, length):
        if x < self.x:
            self.x -= length
            if self.x < x: self.x = x
        self.update()

    def trackVerticalInsert(self, y, length):
        print(y, length)
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

    def down(self, factor = None):
        self.position(*self.ranges.down(factor))

    def endOfBuffer(self):
        self.position(*self.ranges.endOfBuffer())

    def endOfLine(self):
        self.position(*self.ranges.endOfLine())

    def left(self, factor = None):
        self.position(*self.ranges.left(factor))

    def right(self, factor = None):
        self.position(*self.ranges.right(factor))

    def up(self, factor = None):
        self.position(*self.ranges.up(factor))


from .Logger import *
from .Signals import *

class CursorException(Exception): pass

class Cursor:
    """
    * Observes the buffer.
    * Tracks inserting and deleting.
    * Excepts if curser doesn't stay in buffer range.
    * Cursor can stay 1 behing length of line to enable appending.
    * TODO: test exceptions
    """

    def __init__(self):
        self.buffer = None
        self.motions = None
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

    def trackHorizontalInsert(self, x, length):
        if x <= self.x: self.x += length
        self.updated()

    def trackHorizontalDelete(self, x, length):
        if x < self.x:
            self.x -= length
            if self.x < x: self.x = x
        self.updated()

    def trackVerticalInsert(self, y, length):
        print(y, length)
        if y <= self.y: self.y += length
        self.updated()

    def trackVerticalDelete(self, y, length):
        if y < self.y:
            self.y -= length
            if self.y < y: self.y = y
        self.updated()

    def position(self, y = None, x = None):
        if y == None and x == None:
            return (self.y, self.x)
        if y != None: self.y = y
        if x != None: self.x = x
        self.updated()

    def updated(self):
        if self.y < 1:
            raise CursorException("y < range: %s" % self.y)
        if self.y > self.buffer.countOfLines() :
            raise CursorException("y > range: %s > %s" %
                    (self.y, self.buffer.countOfLines()))
        if self.x < 1:
            raise CursorException("x < range: %s" % self.x)
        if self.x > self.buffer.lengthOfLine(self.y) + 1:
            raise CursorException("x > range")
        signal("cursorMoved", self)

    """ Movements """

    def appendInLine(self):
        self.position(*self.motions.appendInLine())

    def beginningOfBuffer(self):
        self.position(*self.motions.beginningOfBuffer())

    def beginningOfLine(self):
        self.position(*self.motions.beginningOfLine())

    def down(self, factor = None):
        self.position(*self.motions.down(factor))

    def endOfBuffer(self):
        self.position(*self.motions.endOfBuffer())

    def endOfLine(self):
        self.position(*self.motions.endOfLine())

    def left(self, factor = None):
        self.position(*self.motions.left(factor))

    def right(self, factor = None):
        self.position(*self.motions.right(factor))

    def up(self, factor = None):
        self.position(*self.motions.up(factor))


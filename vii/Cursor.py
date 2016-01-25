from .Logger import *
from .Signals import *
from .Range import Range, Position

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
        slot("insertedIntoBuffer", self)
        slot("deletedFromBuffer", self)

    def receive(self, signal, sender, **kwargs):
        if sender == self.buffer:
            if signal == "insertedIntoBuffer":
                self.trackDelta(**kwargs)
            if signal == "deletedFromBuffer":
                self.trackDelta(**kwargs)

    def trackDelta(self, **kwargs):
        fromY, fromX = kwargs["startPosition"].toPosition()
        toY, toX = kwargs["afterPosition"].toPosition()
        if(self.y > fromY or
                (self.y == fromY and self.x >= fromX)):
            "cursor after range moves by deltas"
            self.y += toY - fromY
            self.x += toX - fromX
            self.updated()
        elif(self.y > toY or (self.y == toY and self.x > toX)):
            "deleting: cursor in range moves to position of deletion"
            self.y, self.x = toY, toX
            if self.y > self.buffer.countOfLines():
                self.y = self.buffer.countOfLines()
            self.updated()

    def position(self, position = None):
        if position:
            self.y, self.x = position.toPosition()
            self.updated()
        else:
            return Position(self.y, self.x)

    def move(self, range):
        first, second = range.toPositions()
        self.y, self.x = second
        self.updated()

    def updated(self):
        if self.buffer.isEmpty():
            self.x = 1
            self.y = 1
        else:
            if self.y < 1:
                raise CursorException("y < range: %s" % self.y)
            if self.y > self.buffer.countOfLines():
                raise CursorException("y > range: %s > %s" %
                        (self.y, self.buffer.countOfLines()))
            if self.x < 1:
                raise CursorException("x < range: %s" % self.x)
            if self.x > self.buffer.lengthOfLine(self.y) + 1:
                raise CursorException("x > range")
        signal("cursorMoved", self)

    """ Movements """

    def appendInLine(self):
        self.move(self.motions.appendInLine())

    def beginningOfBuffer(self):
        self.move(self.motions.beginningOfBuffer())

    def beginningOfLine(self):
        self.move(self.motions.beginningOfLine())

    def down(self, factor = None):
        self.move(self.motions.down(factor))

    def endOfBuffer(self):
        self.move(self.motions.endOfBuffer())

    def endOfLine(self, count = None):
        self.move(self.motions.endOfLine(count))

    def left(self, factor = None):
        self.move(self.motions.left(factor))

    def right(self, factor = None):
        self.move(self.motions.right(factor))

    def up(self, factor = None):
        self.move(self.motions.up(factor))




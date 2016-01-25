from .Range import Range, Position
from .Logger import debug

class Motions:
    """
    Range control happens here, while the buffer
    is just throwing exectpions.
    """

    def __init__(self):
        self.buffer = None
        self.cursor = None

    def appendInLine(self):
        position = (self._y(), self._x() + 1)
        return (self._toRange(
            self._forceLimits(position, appendX = 1)))

    def beginningOfBuffer(self):
        return self._toRange((1, 1))

    def beginningOfLine(self):
        return self._toRange((self._y(), 1))

    def down(self, step = None):
        if not step: step = 1
        position = self._y() + step, self._x()
        return (self._toRange(
            self._forceLimits(position)))

    def endOfBuffer(self):
        y = self.buffer.countOfLines()
        x = self.buffer.lengthOfLine(y)
        return self._toRange((y, x))

    def endOfLine(self, step = None):
        if not step: step = 1
        y = self._y() + step - 1
        if y > self.buffer.countOfLines():
            y = self.buffer.countOfLines()
        return self._toRange((y, self.buffer.lengthOfLine(y) - 1 ))

    def left(self, step = None):
        if not step: step = 1
        position = (self._y(), self._x() - step)
        return self._toRange(
                self._forceLimits(position))

    def right(self, step = None):
        if not step: step = 1
        position = (self._y(), self._x() + step)
        return self._toRange(
                self._forceLimits(position))

    def up(self, step = None):
        if not step: step = 1
        position = (self._y() - step, self._x())

        return self._toRange(self._forceLimits(position))

    def _x(self):
        return self.cursor.x

    def _y(self):
        return self.cursor.y

    def _forceLimits(self, position, appendX = 0, appendY = 0):
        y, x = position
        countOfLines = self.buffer.countOfLines()
        if countOfLines == 0: return Position(1, 1)
        if y < 1: y = 1
        if x < 1: x = 1
        yLimit = countOfLines + appendY
        if y > yLimit: y = yLimit
        if y > countOfLines:
            x = 1
        else:
            xLimit = self.buffer.lengthOfLine(y) - 1 + appendX
            if x > xLimit: x = xLimit
        return Position(y, x)

    def _toRange(self, position):
        return Range(self.cursor.position(), position)


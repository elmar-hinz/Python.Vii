from .Range import Range
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
            self._forceLimits(position, 1)))

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
        return self._toRange((y, self.buffer.lengthOfLine(y) ))

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
        return self._toRange(
                self._forceLimits(position))

    def _x(self):
        return self.cursor.x

    def _y(self):
        return self.cursor.y

    def _forceLimits(self, position, append = 0):
        y, x = position
        yLimit = self.buffer.countOfLines() + append
        if y > yLimit: y = yLimit
        if y < 1: y = 1
        xLimit = self.buffer.lengthOfLine(y) + append
        if x > xLimit: x = xLimit
        if x < 1: x = 1
        return (y, x)

    def _toRange(self, position):
        return Range(self.cursor.position().toPosition(), position)


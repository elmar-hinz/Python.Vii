
class BufferRanges:
    """
    Range control happens here, while the buffer
    is just throwing exectpions.
    """

    def __init__(self):
        self.buffer = None
        self.cursor = None

    def appendInLine(self):
        range = (self._y(), self._x() + 1)
        return self._forceLimits(range, 1)

    def beginningOfBuffer(self):
        return (1, 1)

    def beginningOfLine(self):
        return (self._y(), 1)

    def down(self, step = None):
        if not step: step = 1
        range = self._y() + step, self._x()
        return self._forceLimits(range)

    def endOfBuffer(self):
        y = self.buffer.countOfLines()
        x = self.buffer.lengthOfLine(y)
        return (y, x)

    def endOfLine(self, step = None):
        if not step: step = 1
        y = self._y() + step - 1
        return (y, self.buffer.lengthOfLine(y) )

    def left(self, step = None):
        if not step: step = 1
        range = (self._y(), self._x() - step)
        return self._forceLimits(range)

    def right(self, step = None):
        if not step: step = 1
        range = (self._y(), self._x() + step)
        return self._forceLimits(range)

    def up(self, step = None):
        if not step: step = 1
        range = (self._y() - step, self._x())
        return self._forceLimits(range)

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


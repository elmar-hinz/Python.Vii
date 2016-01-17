
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
        return (0, 0)

    def beginningOfLine(self):
        return (self._y(), 0)

    def down(self, factor = None):
        if not factor: factor = 1
        range = self._y() + factor, self._x()
        return self._forceLimits(range)

    def endOfBuffer(self):
        y = self.buffer.countOfLines() - 1
        x = self.buffer.lengthOfLine(y) - 1
        return (y, x)

    def endOfLine(self, factor = None):
        if not factor: factor = 1
        y = self._y() + factor - 1
        return (y, self.buffer.lengthOfLine(y) - 1)

    def left(self, factor = None):
        if not factor: factor = 1
        range = (self._y(), self._x() - factor)
        return self._forceLimits(range)

    def right(self, factor = None):
        if not factor: factor = 1
        range = (self._y(), self._x() + factor)
        return self._forceLimits(range)

    def up(self, factor = None):
        if not factor: factor = 1
        range = (self._y() - factor, self._x())
        return self._forceLimits(range)

    def _x(self):
        return self.cursor.x

    def _y(self):
        return self.cursor.y

    def _forceLimits(self, position, append = 0):
        y, x = position
        if y < 0: y = 0
        if x < 0: x = 0

        yLimit = self.buffer.countOfLines() - 1 + append
        if y > yLimit: y = yLimit
        xLimit = self.buffer.lengthOfLine(y) - 1 + append
        if x > xLimit: x = xLimit

        return (y, x)


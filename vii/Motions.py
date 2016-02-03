from .Range import Range, Position
from .Logger import debug

class MotionException(Exception): pass

class Motion(Range):
    def exclusive(self):
        if not self.isTwoPositions():
            raise MotionException("Not two different positions.")
        if self.buffer.lengthOfLine(self.upperY()) == self.upperX():
            raise MotionException("First position is end of line.")
        firstPosition = self.upperPosition()
        if self.lowerX() == 0 or self.lowerX() == 1:
            if self.upperX() == 1 or self.upperX() == 0:
                # exclusive-linewise
                return Range(self.upperY(), self.lowerY() - 1)
            else:
                y = self.lowerY() - 1
                x = self.buffer.lengthOfLine(y) - 1
                lastPosition = Position(y, x)
        else:
            lastPosition = Position(
                self.lastY(), self.lastX() - 1)
        return Range(firstPosition, lastPosition)

class Motions:
    """
    Range control happens here, while the buffer
    is just throwing exectpions.

    Range doesn't control the start position,
    because the movement may happen as result
    of a deletion, after which the start position
    doesn't exist any more.

    Start positons are 1, 0 for empty lines or buffer.
    """

    def __init__(self):
        self.buffer = None
        self.cursor = None
        self.search = None

    def gotoPositionStrict(self, position):
        return self._toRange(position.toPositionTuple())

    def gotoPositionRelaxed(self, position):
        return self._toRange(
            position.toPositionTuple(), appendX = 1)

    def appendInLine(self):
        position = (self._y(), self._x() + 1)
        return self._toRange(position, appendX = 1)

    def beginningOfBuffer(self):
        return self._toRange((1,1))

    def beginningOfLine(self):
        return self._toRange((self._y(), 1))

    def down(self, step = None):
        if step == None: step = 1
        position = self._y() + step, self._x()
        return self._toRange(position)

    def endOfBuffer(self):
        y = self.buffer.countOfLines()
        x = self.buffer.lengthOfLine(y) - 1
        return self._toRange((y, x))

    def endOfLine(self, step = None):
        if step == None: step = 1
        if step == 0: step = 1
        y = self._y() + step - 1
        if y > self.buffer.countOfLines():
            y = self.buffer.countOfLines()
        return self._toRange((y, self.buffer.lengthOfLine(y) - 1 ))

    def left(self, step = None):
        if step == None: step = 1
        position = (self._y(), self._x() - step)
        return self._toRange(position)

    def right(self, step = None):
        if step == None: step = 1
        position = (self._y(), self._x() + step)
        return self._toRange(position)

    def up(self, step = None):
        if step == None: step = 1
        position = (self._y() - step, self._x())
        return self._toRange(position)

    def find(self, pattern, range,
            step = None, backwards = False,
            matchEmptyLines = False):
        if step == None: step = 1
        results = self.search.search(
            pattern = pattern, range = range,
            matchEmptyLines = matchEmptyLines)
        if len(results) < 1:
            position = self.cursor.position()
            return self._toRange(position.toPositionTuple())
        if backwards:
            step = -step
            if results[-1].position == self.cursor.position():
                step -= 1
            fallbackPosition = 0
        else:
            if results[0].position != self.cursor.position():
                step -= 1
            fallbackPosition = -1
        try:
            position = results[step].position
        except IndexError:
            position = results[fallbackPosition].position
        return self._toRange(position.toPositionTuple())

    def _x(self):
        return self.cursor.x

    def _y(self):
        return self.cursor.y

    # TODO accept Position instead of tuple
    def _toRange(self, position, appendX = 0):
        position = self._forceLimits(position, appendX)
        motion = Motion(self.cursor.position(), position)
        motion.buffer = self.buffer
        return motion

    def _forceLimits(self, position, appendX = 0):
        y, x = position
        countOfLines = self.buffer.countOfLines()
        if countOfLines == 0: return Position(0,0)
        if y < 1: y = 1
        if y > countOfLines: y = countOfLines
        lengthOfLine = self.buffer.lengthOfLine(y)
        if lengthOfLine == 1:
            x = 0
        elif lengthOfLine > 1:
            if x < 1: x = 1
            xLimit = lengthOfLine - 1 + appendX
            if x > xLimit: x = xLimit
        else:
            raise Exception("Never reached")
        return Position(y, x)


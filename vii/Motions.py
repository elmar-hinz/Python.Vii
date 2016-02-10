from .Range import Range, Position
from .Logger import debug

class MotionException(Exception): pass

class Motion(Range):
    """
    Provides tools to adjust the motion for different tasks.

    Motions don't control the start position,
    because the movement may happen as result
    of a deletion, after which the start position
    doesn't exist any more.

    Indexes start by 1, 0 for empty lines or buffer.
    """

    def swap(self):
        motion = Motion(self.position2, self.position1)
        motion.buffer = self.buffer
        return motion

    def limitVertical(self):
        y = self.lastY()
        if y < 1: y = 1
        if y > self.buffer.countOfLines():
            y = self.buffer.countOfLines()
        motion = Motion(self.firstPosition(),
                Position(y,self.lastX()))
        motion.buffer = self.buffer
        return motion

    def forceLimits(self, appendX = 0):
        y, x = self.lastPosition().toPositionTuple()
        countOfLines = self.buffer.countOfLines()
        if countOfLines == 0:
            motion = Motion(self.firstPosition(),
                    Position(0,0))
            motion.buffer = self.buffer
            return motion
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
        motion = Motion(self.firstPosition(),
                Position(y,x))
        motion.buffer = self.buffer
        return motion

    def exclusive(self):
        """ keeps order of first and last position """
        if not self.isTwoPositions():
            return None
        if self.buffer.lengthOfLine(self.upperY()) == self.upperX():
            raise MotionException("First position is end of line.")
        if self.isInverse():
            motion = self.swap()
            wasInverse = True
        else:
            motion = self
            wasInverse = False
        firstPosition = motion.upperPosition()
        if(motion.upperY() != motion.lowerY()
                and (motion.lowerX() == 0 or motion.lowerX() == 1)):
            if motion.upperX() == 1 or motion.upperX() == 0:
                # exclusive-linewise
                y = motion.upperY() - 1
                x = motion.buffer.lengthOfLine(y) - 1
                lastPosition = Position(y, x)
            else:
                y = motion.lowerY() - 1
                x = motion.buffer.lengthOfLine(y) - 1
                lastPosition = Position(y, x)
        else:
            lastPosition = Position(
                motion.lowerY(), motion.lowerX() - 1)
        motion = Motion(firstPosition, lastPosition)
        motion.buffer = self.buffer
        if wasInverse: motion = motion.swap()
        return motion

class Motions:
    """
    The created movements are "raw". They are
    not adjusted to buffer ranges. They are not
    exclusive.

    Use the tools of Motion to adjust the raw
    motion for the very task.

    However, motions that directly address buffer ranges, like
    beginningOfBuffer, endOfBuffer, beginningOfLine, endOfLine
    are adjusted to a certain degree.
    """

    def __init__(self):
        self.buffer = None
        self.cursor = None
        self.search = None

    def appendInLine(self):
        position = Position(self._y(), self._x() + 1)
        return self.makeMotion(position)

    def beginningOfBuffer(self):
        if not self.buffer.isEmpty():
            position = Position(1,1)
        else:
            position = Position(0,0)
        return self.makeMotion(position)

    def beginningOfLine(self):
        if self.buffer.lengthOfLine(self._y()) < 2:
            position = Position(self._y(), 0)
        else:
            position = Position(self._y(), 1)
        return self.makeMotion(position)

    def down(self, step = None):
        if step == None: step = 1
        position = Position(self._y() + step,
                self._x())
        return self.makeMotion(position)

    def endOfBuffer(self):
        position = self.buffer.lastPosition()
        return self.makeMotion(position)

    def endOfLine(self, step = None):
        if step == None: step = 1
        if step == 0: step = 1
        y = self._y() + step - 1
        if y > self.buffer.countOfLines():
            position = self.buffer.lastPosition()
        else:
            position = self.buffer.lastPositionInLine(y)
        return self.makeMotion(position)

    def left(self, step = None):
        if step == None: step = 1
        position = Position(self._y(), self._x() - step)
        return self.makeMotion(position)

    def right(self, step = None):
        if step == None: step = 1
        position = Position(self._y(), self._x() + step)
        return self.makeMotion(position)

    def up(self, step = None):
        if step == None: step = 1
        position = Position(self._y() - step, self._x())
        return self.makeMotion(position)

    def find(self, pattern, range,
            step = None, backwards = False,
            matchEmptyLines = False,
            matchRangeBorders = True):
        if step == None: step = 1
        results = self.search.search(
            pattern = pattern, range = range,
            matchEmptyLines = matchEmptyLines)
        positions = []
        for result in results:
            positions.append(result.position)
        if matchRangeBorders:
            if backwards and (len(positions) == 0
                    or positions[0] != range.upperPosition()):
                positions = [range.upperPosition()] + positions
            elif(len(positions) == 0
                    or positions[-1] != range.lowerPosition()):
                positions += [range.lowerPosition()]
        if len(positions) < 1:
            position = self.cursor.position()
            return self.makeMotion(position)
        if backwards:
            step = -step
            if positions[-1] == self.cursor.position():
                step -= 1
            fallbackPosition = 0
        else:
            if positions[0] != self.cursor.position():
                step -= 1
            fallbackPosition = -1
        try:
            position = results[step].position
        except IndexError:
            position = positions[fallbackPosition]
        return self.makeMotion(position)

    def _x(self):
        return self.cursor.x

    def _y(self):
        return self.cursor.y

    def makeMotion(self, position):
        motion = Motion(self.cursor.position(), position)
        motion.buffer = self.buffer
        return motion


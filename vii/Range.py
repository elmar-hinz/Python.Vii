
class NotLinesRangeException(Exception): pass
class NotOneLineRangeException(Exception): pass
class NotTwoLinesRangeException(Exception): pass
class NotPositionsRangeException(Exception): pass
class NotOnePositionRangeException(Exception): pass
class NotTwoPositionsRangeException(Exception): pass

class Range:
    """
    Ranges are immutable. No copy function is needed.
    By design no manipulations. Getters return new
    objects where needed.
    """

    def __init__(self, *args, isPosition = False):
        newArgs = []
        for i in range(len(args)):
            if (isinstance(args[i], Range)
                    and args[i].isOnePosition()):
                newArgs.append(args[i].toPositionTuple())
            else:
                newArgs.append(args[i])
        args = tuple(newArgs)
        if (len(args) == 1
                and isinstance(args[0], int)):
            self.position1 = (args[0], None)
            self.position2 = (args[0], None)
            """ is one line """
        elif (len(args) == 1
                and len(args[0]) == 2
                and not isPosition):
            """ is two lines """
            self.position1 = (args[0][0], None)
            self.position2 = (args[0][1], None)
        elif (len(args) == 1
                and len(args[0]) == 2
                and isPosition):
            """ is one position """
            self.position1 = args[0]
            self.position2 = args[0]
        elif len(args) == 2:
            if(isinstance(args[0], int)
                    and isinstance(args[1], int)):
                if isPosition:
                    """ is one position """
                    self.position1 = args
                    self.position2 = args
                else:
                    """ is lines """
                    self.position1 = (args[0], None)
                    self.position2 = (args[1], None)
            elif len(args[0]) == 2 and len(args[1]) == 2:
                """ is positions """
                self.position1 = args[0]
                self.position2 = args[1]

    def __eq__(self, other):
        return (self.position1 == other.position1
            and self.position2 == other.position2)

    def __str__(self):
        return ("Range: %s, %s : %s, %s" %
                (*self.position1, *self.position2))

    def isInverse(self):
        if self.position1[0] > self.position2[0]:
            return True
        if(self.isPositions()
                and self.position1[0] == self.position2[0]
                and self.position1[1] > self.position2[1]):
            return True
        return False

    def isLines(self):
        return (self.position1[1] == None
            and self.position2[1] == None)

    def isOneLine(self):
        return (self.isLines()
            and self.position1 == self.position2)

    def isTwoLines(self):
        return (self.isLines()
            and self.position1 != self.position2)

    def isPositions(self):
        return (self.position1[1] != None
            and self.position2[1] != None)

    def isOnePosition(self):
        return (self.isPositions()
            and self.position1 == self.position2)

    def isTwoPositions(self):
        return (self.isPositions()
            and self.position1 != self.position2)

    def assertLines(self):
        if not self.isLines():
            raise NotLinesRangeException()

    def assertOneLine(self):
        if not self.isOneLine():
            raise NotOneLineRangeException()

    def assertTwoLines(self):
        if not self.isTwoLines():
            raise NotTwoLinesRangeException()

    def assertPositions(self):
        if not self.isPositions():
            raise NotPositionsRangeException()

    def assertOnePosition(self):
        if not self.isOnePosition():
            raise NotOnePositionRangeException()

    def assertTwoPositions(self):
        if not self.isTwoPositions():
            raise NotTwoPositionsRangeException()

    def contains(self, position):
        position.assertOnePosition()
        y, x = position.toPositionTuple()
        if y < self.upperY():
            return False
        elif y > self.lowerY():
            return False
        elif(   y == self.upperY()
                and self.upperX() != None
                and x < self.upperX()):
            return False
        elif(   y == self.lowerY()
                and self.lowerX() != None
                and x > self.lowerX()):
            return False
        else:
            return True

    # Getters

    def toLineTuples(self):
        return self.position1[0], self.position2[0]

    def toPositionTuple(self):
        self.assertPositions()
        return self.position1

    def toPositionTuples(self):
        self.assertPositions()
        return self.position1, self.position2

    def firstPosition(self):
        return Range(self.position1, isPosition = True)

    def firstY(self):
            return self.position1[0]

    def firstX(self):
            return self.position1[1]

    def lastPosition(self):
        return Range(self.position2, isPosition = True)

    def lastX(self):
            return self.position2[1]

    def lastY(self):
            return self.position2[0]

    def linewise(self):
        return Range(self.position1[0], self.position2[0])

    def lowerPosition(self):
        if self.isInverse():
            return self.firstPosition()
        else:
            return self.lastPosition()

    def lowerX(self):
        if self.isInverse():
            return self.position1[1]
        else:
            return self.position2[1]

    def lowerY(self):
        if self.isInverse():
            return self.position1[0]
        else:
            return self.position2[0]

    def swap(self):
        return Range(self.position2, self.position1)

    def upperPosition(self):
        if self.isInverse():
            return self.lastPosition()
        else:
            return self.firstPosition()

    def upperX(self):
        if self.isInverse():
            return self.position2[1]
        else:
            return self.position1[1]

    def upperY(self):
        if self.isInverse():
            return self.position2[0]
        else:
            return self.position1[0]

class Position(Range):
    def __init__(self, x, y):
        super().__init__(x, y, isPosition = True)



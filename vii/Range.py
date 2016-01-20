
class NotLinesRangeException(Exception): pass
class NotOneLineRangeException(Exception): pass
class NotTwoLinesRangeException(Exception): pass
class NotPositionsRangeException(Exception): pass
class NotOnePositionRangeException(Exception): pass
class NotTwoPositionsRangeException(Exception): pass

class Range:

    def __init__(self, *args, isPosition = False):
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

    def toLine(self):
        return self.position1[0]

    def toLines(self):
        return self.position1[0], self.position2[0]

    def toPosition(self):
        self.assertPositions()
        return self.position1

    def toPositions(self):
        self.assertPositions()
        return self.position1, self.position2


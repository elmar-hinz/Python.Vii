
class Range:

    def __init__(self, *args, isPosition = False):
        if (len(args) == 1
                and len(args[0]) == 2
                and isPosition):
            """ is one position """
            self.position1 = args[0]
            self.position2 = args[0]
        elif (len(args) == 1
                and len(args[0]) == 2
                and not isPosition):
            """ is lines """
            self.position1 = (args[0][0], None)
            self.position2 = (args[0][1], None)
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

    def isOnePositon(self):
        return (self.position1 == self.position2
                and self.position1[1] != None)

    def toPosition(self):
        return self.position1

    def toLines(self):
        return self.position1[0], self.position2[0]

    def toPositions(self):
        return self.position1, self.position2



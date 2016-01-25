from .Signals import signal
from .Range import Range, Position
from .Logger import *

class BufferBoundsException(IndexError): pass
class LineBoundsException(IndexError): pass
class RangeExeption(IndexError): pass
class LastLinebreakLostExecption(Exception): pass

class Buffer:
    """
    All ranges are inclusive, no null range possible.

    Indexing of all functions is based on 1
    for y and x while the internal lines array
    is based on 0 as usual in Python.

    The y direction (linewise) is always named
    before x.

    Every line ends with "\n".
    Empty lines contain just  "\n".
    For zero lines __str__ returns "".
    Line length includes the linebreak.

    Operations are rejected with an exception,
    if they cauuse a missing "\n" at the end
    of the last line.
    """

    filledSignal = "filledBuffer"
    deletedSignal = "deletedFromBuffer"
    insertedSignal = "insertedIntoBuffer"
    updatedSignal = "updatedBuffer"

    def __init__(self):
        self.lines = []
        signal(self.updatedSignal, self)

    def insert(self, position, string):
        "Insert string at position y, x"
        "plus 1 in y or x for appending"
        if string == "": return
        y, x = position.toPosition()
        tokens = self._parse(string)
        try: head = self.lines[y-1][:x-1]
        except IndexError: head = ""
        try: tail = self.lines[y-1][x-1:]
        except IndexError: tail = ""

        if tail and tokens[-1][-1] == "\n":
            tokens.append("")
        tokens[0] = head + tokens[0]
        tokens[-1] = tokens[-1] + tail
        length = self.countOfLines()
        if(y in (length, length + 1)
            and tokens[-1][-1] != "\n"):
                raise LastLinebreakLostExecption()
        self.lines[y-1:y] = tokens

        afterX = len(tokens[-1]) - len(tail) + 1
        afterY = y + len(tokens) - 1
        signal(self.insertedSignal, self,
            startPosition=position,
            afterPosition=Position(afterY,afterX))
        signal(self.updatedSignal, self)

    def copy(self, range):
        if self.isEmpty(): return ""
        range = self._resolveRange(range)
        (y1, x1), (y2, x2) = range.toPositions()
        if y1 == y2:
            return self.lines[y1-1][x1-1:x2]
        else:
            head = self.lines[y1-1][x1-1:]
            tail = self.lines[y2-1][:x2]
            body = self._join(self.lines[y1:y2-1])
            return head + body + tail

    def delete(self, range):
        if self.isEmpty(): return
        range = self._resolveRange(range)
        (y1, x1), (y2, x2) = range.toPositions()
        head = self.lines[y1-1][:x1-1]
        tail = self.lines[y2-1][x2:]
        if not tail:
            y2 = y2 + 1
            x2 = 0
            try: tail = self.lines[y2 - 1]
            except IndexError: tail = ""
        string = head + tail
        if string:
            if string[-1] != "\n":
                raise LastLinebreakLostExecption()
            self.lines[y1-1:y2] = [string]
        else:
            self.lines[y1-1:y2] = []
        startY = y2
        startX = x2 + 1
        debug(self.lines)
        signal(self.deletedSignal, self,
            startPosition=Position(startY,startX),
            afterPosition=Position(y1, x1))
        signal(self.updatedSignal, self)

    def isEmpty(self):
        "Has Zero lines"
        return (len(self.lines) == 0)

    def characterCount(self):
        "Character count"
        count = 0
        for line in self.lines: count += len(line)
        return count

    def lengthOfLine(self, y):
        "Length of line including linebreak"
        self._checkBufferBounds(y)
        return len(self.lines[y-1])

    def countOfLines(self):
        "Count of lines"
        return len(self.lines)

    def fill(self, text):
        "Clear and fill the buffer with text"
        if text == "": return
        if text[-1] != "\n":
            raise LastLinebreakLostExecption()
        self.lines = self._parse(text)
        signal(self.filledSignal, self)
        signal(self.updatedSignal, self)

    def _parse(self, string):
        "Parse to list of lines"
        if string == "": return []
        lines = string.splitlines()
        for i in range(len(lines) - 1):
            lines[i] += "\n"
        if string[-1] == "\n":
            lines[-1] += "\n"
        return lines

    def _join(self, lines):
        "Join str from list of lines"
        return "".join(lines)

    def __str__(self):
        return self._join(self.lines)

    def _resolveRange(self, range):
        if range.isInverse(): range = range.swap()
        if range.isLines():
            y1, y2 = range.toLines()
            start = (y1, 1)
            stop = (y2, self.lengthOfLine(y2))
            range = Range(start, stop)
        return range

    def _checkBufferBounds(self, y, plus = 0):
        if y < 1:
            raise BufferBoundsException()
        if y > len(self.lines) + plus:
            raise BufferBoundsException()

    def _checkLineBounds(self, y, x):
        self._checkBufferBounds(y)
        if x < 1:
            raise LineBoundsException("1: y/x: %s/%s"%(y,x))
        line = self.lines[y-1]
        if x > len(line):
            raise LineBoundsException("2: y/x: %s/%s"%(y,x))

    def _checkLineBoundsPlus1(self, y, x):
        self._checkBufferBounds(y)
        if x < 1:
            raise LineBoundsException("3: y/x: %s/%s"%(y,x))
        line = self.lines[y-1]
        if x > len(line) + 1:
            raise LineBoundsException("4: y/x: %s/%s"%(y,x))

    def _checkRange(self, start, end):
        y1, x1 = start; y2, x2 = end

        if y1 > y2: raise RangeExeption()
        if y1 == y2 and x1 > x2: raise RangeExeption()
        self._checkLineBounds(y1, x1)
        self._checkLineBounds(y2, x2)
        return ((y1, x1), (y2, x2))


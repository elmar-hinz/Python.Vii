from .Signals import signal

class BufferBoundsException(IndexError): pass
class LineBoundsException(IndexError): pass
class RangeExeption(IndexError): pass

class Buffer:
    """
    All ranges are inclusive.

    Indexing of all functions is based on 1
    for y and x while the internal lines array
    is based on 0 as usual in Python.

    The y direction (linewise) is always named
    before x.
    """

    updateSignal = "bufferUpdate"

    def __init__(self):
        self.lines = []
        signal(self.updateSignal, self)

    def insert(self, position, string):
        "Insert string at position y, x"
        "Plus1 for appending"
        if string == "": return
        y, x = position
        self._checkLineBoundsPlus1(y, x)
        tokens = self._parse(string)
        head = self.lines[y-1][:x-1]
        tail = self.lines[y-1][x-1:]
        if len(tokens) == 1:
            body = tokens[0]
            replacement = [head + body + tail]
        else:
            head = head + tokens[0]
            body = tokens[1:-1]
            tail = tokens[-1] + tail
            replacement = [head] + body + [tail]
        self.lines[y-1:y] = replacement
        signal(self.updateSignal, self)

    def insertLines(self, y, text):
        "Insert text at y as full lines"
        "Plus1 for appending"
        self._checkBufferBoundsPlus1(y)
        self.lines[y-1:y-1] = self._parse(text)
        signal(self.updateSignal, self)

    def deleteFromLine(self, position, count):
        "Delete count chars from position"
        if count == 0: return
        y, x = position
        self._checkLineBounds(y, x)
        self._checkLineBounds(y, x + count - 1)
        line = self.lines[y-1]
        self.lines[y-1] = line[:x-1] + line[x-1+count:]
        signal(self.updateSignal, self)

    def deleteLines(self, y, count):
        if count == 0: return
        self._checkBufferBounds(y)
        self._checkBufferBounds(y+count-1)
        self.lines[y-1:y-1+count] = []
        "Delete count lines from y"
        signal(self.updateSignal, self)

    def deleteRange(self, start, end):
        "Delete from position to position"
        start, end = self._checkRange(start, end)
        y1, x1 = start; y2, x2 = end
        head = self.lines[y1-1][:x1-1]
        tail = self.lines[y2-1][x2-1+1:]
        self.lines[y1-1:y2] = [head + tail]
        signal(self.updateSignal, self)

    def copyFromLine(self, position, count):
        "Copy count chars from position"
        if count == 0: return ""
        y, x = position
        self._checkLineBounds(y, x)
        self._checkLineBounds(y, x + count - 1)
        return self.lines[y-1][x-1:x-1+count]

    def copyLines(self, y, count):
        "Copy count lines from y"
        if count == 0: return ""
        self._checkBufferBounds(y)
        self._checkBufferBounds(y + count - 1)
        return self._join(self.lines[y-1:y-1+count])

    def copyRange(self, start, end):
        "Copy from position to position"
        start, end = self._checkRange(start, end)
        y1, x1 = start; y2, x2 = end
        if y1 == y2:
            count = x2 - x1 + 1
            return self.copyFromLine(start, count)
        else:
            count = self.lengthOfLine(y1) - x1 + 1
            head = self.copyFromLine(start, count)
            tail = self.copyFromLine((y2, 1), x2)
            if y2 - y1 >= 2:
                body = self.copyLines(y1 + 1, y2 - y1 - 1)
                return '\n'.join([head, body, tail])
            else:
                return '\n'.join([head, tail])

    def lengthOfLine(self, y):
        "Length of line y"
        self._checkBufferBounds(y)
        return len(self.lines[y-1])

    def countOfLines(self):
        "Count of lines"
        return len(self.lines)

    def fill(self, text):
        "Clear and fill the buffer with text"
        self.deleteLines(1, self.countOfLines())
        self.insertLines(1, text)

    def _parse(self, string):
        "Parse to list of lines"
        lines = string.splitlines()
        if lines == []: lines = [""]
        elif string[-1] == '\n': lines += [""]
        return lines

    def _join(self, lines):
        "Join str from list of lines"
        return "\n".join(lines)

    def __str__(self):
        return self._join(self.lines)

    def _checkBufferBounds(self, y):
        if y < 1:
            raise BufferBoundsException()
        if y > len(self.lines):
            raise BufferBoundsException()

    def _checkBufferBoundsPlus1(self, y):
        if y < 1:
            raise BufferBoundsException()
        if y > len(self.lines) + 1:
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


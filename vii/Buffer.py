from .Signals import signal

class BufferBoundsException(IndexError): pass
class LineBoundsException(IndexError): pass
class RangeExeption(IndexError): pass

class Buffer:
    """
    All ranges are inclusive.
    """

    updateSignal = "bufferUpdate"

    def __init__(self):
        self.lines = []
        signal(self.updateSignal, self)

    def insert(self, position, string):
        "Insert string at position y, x"
        if string == "": return
        y, x = position
        self._checkLineBoundsPlus1(y, x)
        tokens = self._parse(string)
        head = self.lines[y][:x]
        tail = self.lines[y][x:]
        if len(tokens) == 1:
            body = tokens[0]
            replacement = [head + body + tail]
        else:
            head = head + tokens[0]
            body = tokens[1:-1]
            tail = tokens[-1] + tail
            replacement = [head] + body + [tail]
        self.lines[y:y+1] = replacement
        signal(self.updateSignal, self)

    def insertLines(self, y, text):
        "Insert text at y as full lines"
        self._checkBufferBoundsPlus1(y)
        self.lines[y:y] = self._parse(text)
        signal(self.updateSignal, self)

    def deleteFromLine(self, position, count):
        "Delete count chars from position"
        if count == 0: return
        y, x = position
        self._checkLineBounds(y, x)
        self._checkLineBounds(y, x + count - 1)
        line = self.lines[y]
        self.lines[y] = line[:x] + line[x+count:]
        signal(self.updateSignal, self)

    def deleteLines(self, y, count):
        if count == 0: return
        self._checkBufferBounds(y)
        self._checkBufferBounds(y+count-1)
        self.lines[y:y+count] = []
        "Delete count lines from y"
        signal(self.updateSignal, self)

    def deleteRange(self, start, end):
        "Delete from position to position"
        self._checkRange(start, end)
        y1, x1 = start; y2, x2 = end
        head = self.lines[y1][:x1]
        tail = self.lines[y2][x2+1:]
        self.lines[y1:y2+1] = [head + tail]
        signal(self.updateSignal, self)

    def copyFromLine(self, position, count):
        "Copy count chars from position"
        if count == 0: return ""
        y, x = position
        self._checkLineBounds(y, x)
        self._checkLineBounds(y, x + count - 1)
        return self.lines[y][x:x+count]

    def copyLines(self, y, count):
        "Copy count lines from y"
        if count == 0: return ""
        self._checkBufferBounds(y)
        self._checkBufferBounds(y + count - 1)
        return self._join(self.lines[y:y+count])

    def copyRange(self, start, end):
        "Copy from position to position"
        self._checkRange(start, end)
        y1, x1 = start; y2, x2 = end
        if y1 == y2:
            count = x2 - x1 + 1
            return self.copyFromLine(start, count)
        else:
            count = self.lengthOfLine(y1) - x1
            head = self.copyFromLine(start, count)
            tail = self.copyFromLine((y2, 0), x2 + 1)
            if y2 - y1 >= 2:
                body = self.copyLines(y1 + 1, y2 - y1 - 1)
                return '\n'.join([head, body, tail])
            else:
                return '\n'.join([head, tail])

    def lengthOfLine(self, y):
        "Length of line y"
        self._checkBufferBounds(y)
        return len(self.lines[y])

    def countOfLines(self):
        "Count of lines"
        return len(self.lines)

    def fill(self, text):
        "Clear and fill the buffer with text"
        self.deleteLines(0, self.countOfLines())
        self.insertLines(0, text)

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
        if y < 0:
            raise BufferBoundsException()
        if y >= len(self.lines):
            raise BufferBoundsException()

    def _checkBufferBoundsPlus1(self, y):
        if y < 0:
            raise BufferBoundsException()
        if y > len(self.lines):
            raise BufferBoundsException()

    def _checkLineBounds(self, y, x):
        self._checkBufferBounds(y)
        if x < 0:
            raise LineBoundsException("1: y/x: %s/%s"%(y,x))
        line = self.lines[y]
        if x >= len(line):
            raise LineBoundsException("2: y/x: %s/%s"%(y,x))

    def _checkLineBoundsPlus1(self, y, x):
        self._checkBufferBounds(y)
        if x < 0:
            raise LineBoundsException("3: y/x: %s/%s"%(y,x))
        line = self.lines[y]
        if x > len(line):
            raise LineBoundsException("4: y/x: %s/%s"%(y,x))

    def _checkRange(self, start, end):
        y1, x1 = start; y2, x2 = end
        self._checkLineBounds(y1, x1)
        self._checkLineBounds(y2, x2)
        if y1 > y2: raise RangeExeption()
        if y1 == y2 and x1 > x2: raise RangeExeption()

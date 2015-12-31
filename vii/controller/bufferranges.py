
class BufferRanges:
    """
    Calculate the end position of each range.
    The current position is taken form cursor.
    Values out of range of the buffer are possible.
    Range controll happens in the buffer itself.
    """

    def __init__(self, buffer, cursor):
        self.buffer = buffer
        self.cursor = cursor

    def beginningOfBuffer(self):
        return (0, 0)

    def beginningOfLine(self):
        return (self._y(), 0)

    def down(self):
        return (self._y() + 1, self._x())

    def endOfBuffer(self):
        y = len(self.buffer) - 1
        x = len(self.buffer[y]) - 1
        return (y, x)

    def endOfLine(self):
        return (self._y(), len(self._line()) - 1)

    def left(self):
        return (self._y(), self._x() - 1)

    def right(self):
        return (self._y(), self._x() + 1)

    def up(self):
        return (self._y() - 1, self._x())

    def _line(self):
        return self.buffer[self._y()]

    def _x(self):
        return self.cursor.x

    def _y(self):
        return self.cursor.y


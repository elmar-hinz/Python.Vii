from .Cursor import Cursor
from .BufferRanges import BufferRanges
from .Logger import *
from .Setup import numberBarWidth, commandMap

class NormalActions:

    buffer, cursor, move = None, None, None

    def __init__(self, buffer, cursor):
        self.buffer = buffer
        self.cursor = cursor
        self.move = BufferRanges(buffer, cursor)

    def append(self, command):
        self.cursor.position(*self._append(self.cursor.position()))
        return "InsertMode"

    def insert(self, command):
        return "InsertMode"

    def up(self, command):
        for i in range(command.count()):
            self.cursor.position(*self.move.up())

    def down(self, command):
        for i in range(command.count()):
            self.cursor.position(*self.move.down())

    def left(self, command):
        for i in range(command.count()):
            self.cursor.position(*self.move.left())

    def right(self, command):
        for i in range(command.count()):
            self.cursor.position(*self.move.right())

    def endOfLine(self, command):
        self.cursor.position(*self.move.endOfLine())

    def beginningOfLine(self, command):
        self.cursor.position(*self.move.beginningOfLine())

    def appendToLine(self, command):
        self.cursor.position(*self._append(self.move.endOfLine()))
        return "InsertMode"

    def insertBeforeLine(self, command):
        self.cursor.position(*self.move.beginningOfLine())
        return "InsertMode"

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)


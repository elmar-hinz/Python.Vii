from .AbstractAction import AbstractAction
from .Cursor import Cursor
from .BufferRanges import BufferRanges
from .Logger import *

class Idle(AbstractAction):

    def act(self):
        debug("Idle")
        pass

class Append(AbstractAction):

    def act(self):
        self.cursor.position(*self._append(self.cursor.position()))
        return "InsertMode"

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)

class Insert(AbstractAction):

    def act(self):
        return "InsertMode"

class Up(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.up())

class Down(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.down())

class Left(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.left())

class Right(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.right())

class BeginningOfLine(AbstractAction):

    def act(self):
        self.cursor.position(*self.move.beginningOfLine())

class EndOfLine(AbstractAction):

    def act(self):
        self.cursor.position(*self.move.endOfLine())

class AppendToLine(AbstractAction):

    def act(self):
        self.cursor.position(*self._append(self.move.endOfLine()))
        return "InsertMode"

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)

class InsertBeforeLine(AbstractAction):

    def act(self):
        self.cursor.position(*self.move.beginningOfLine())
        return "InsertMode"


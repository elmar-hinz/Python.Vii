from .AbstractAction import AbstractAction
from .Cursor import Cursor
from .BufferRanges import BufferRanges
from .Logger import *

class Idle(AbstractAction):

    def act(self):
        if self.dispatcher.ready():
            operator = self.dispatcher.operator()
            return self.actionManager.action("normal", operator)[1].act()
        else:
            return "normal", self

class Append(AbstractAction):

    def act(self):
        self.cursor.position(*self._append(self.cursor.position()))
        return self.actionManager.action("insert", "inserting")

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)

class Insert(AbstractAction):

    def act(self):
        return self.actionManager.action("insert", "inserting")

class Up(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.up())
        self.finish()
        return self.actionManager.action("normal", "idle")

class Down(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.down())
        self.finish()
        return self.actionManager.action("normal", "idle")

class Left(AbstractAction):

    def act(self):
        debug("Left")
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.left())
        self.finish()
        return self.actionManager.action("normal", "idle")

class Right(AbstractAction):

    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.right())
        self.finish()
        return self.actionManager.action("normal", "idle")

class BeginningOfLine(AbstractAction):

    def act(self):
        self.cursor.position(*self.move.beginningOfLine())
        self.finish()
        return self.actionManager.action("normal", "idle")

class EndOfLine(AbstractAction):

    def act(self):
        self.cursor.position(*self.move.endOfLine())
        self.finish()
        return self.actionManager.action("normal", "idle")

class AppendToLine(AbstractAction):

    def act(self):
        self.cursor.position(*self._append(self.move.endOfLine()))
        return self.actionManager.action("insert", "inserting")

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)

class InsertBeforeLine(AbstractAction):

    def act(self):
        self.cursor.position(*self.move.beginningOfLine())
        return self.actionManager.action("insert", "inserting")


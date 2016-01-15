from .AbstractAction import AbstractAction
from .Logger import *

class Idle(AbstractAction):
    def act(self):
        if self.dispatcher.ready():
            operator = self.dispatcher.operator()
            return self.actionManager.action("normal", operator).act()
        else:
            return "normal", self

class Append(AbstractAction):
    def act(self):
        self.cursor.position(*self._append(self.cursor.position()))
        return "insert", self.actionManager.action("insert", "inserting")

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)

class Insert(AbstractAction):
    def act(self):
        return "insert", self.actionManager.action("insert", "inserting")

class Up(AbstractAction):
    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.up())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Down(AbstractAction):
    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.down())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Left(AbstractAction):
    def act(self):
        self.cursor.position(*self.move.left(self.dispatcher.count()))
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Right(AbstractAction):
    def act(self):
        for i in range(self.dispatcher.count()):
            self.cursor.position(*self.move.right())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class BeginningOfLine(AbstractAction):
    def act(self):
        self.cursor.position(*self.move.beginningOfLine())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class EndOfLine(AbstractAction):
    def act(self):
        self.cursor.position(*self.move.endOfLine())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class AppendToLine(AbstractAction):
    def act(self):
        self.cursor.position(*self._append(self.move.endOfLine()))
        return "insert", self.actionManager.action("insert", "inserting")

    @staticmethod
    def _append(position):
        return (position[0], position[1] + 1)

class InsertBeforeLine(AbstractAction):
    def act(self):
        self.cursor.position(*self.move.beginningOfLine())
        return "insert", self.actionManager.action("insert", "inserting")

class Yank(AbstractAction):
    def act(self):
        return self.actionManager.action("operatorPending", "yank").act()

class Delete(AbstractAction):
    def act(self):
        return self.actionManager.action("operatorPending", "delete").act()

class Change(AbstractAction):
    def act(self):
        return self.actionManager.action("operatorPending", "change").act()


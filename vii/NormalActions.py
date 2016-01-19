from .AbstractAction import AbstractAction
from .AbstractAction import AbstractPendingAction
from .Logger import *

class Idle(AbstractAction):
    def act(self, dummyCallback = None):
        """ dummy callback required when used as Null
        action from operartor pending mode. """
        if self.command.cpReady():
            operator = self.command.cpOperator()
            return self.actionManager.action("normal", operator).act()
        else:
            return "normal", self

class Append(AbstractAction):
    def act(self):
        self.cursor.appendInLine()
        self.command.next()
        return "insert", self.actionManager.action("insert", "inserting")

class AppendToLine(AbstractAction):
    def act(self):
        self.cursor.endOfLine()
        self.cursor.appendInLine()
        self.command.next()
        return "insert", self.actionManager.action("insert", "inserting")

class BeginningOfLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Change(AbstractPendingAction):
    def call(self, range):
        self.buffer.deleteRange(*range)
        self.command.next()
        return "insert", self.actionManager.action("insert", "inserting")

class Delete(AbstractPendingAction):
    def call(self, range):
        self.buffer.deleteRange(*range)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Down(AbstractAction):
    def act(self):
        self.cursor.down(self.command.cpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class EndOfLine(AbstractAction):
    def act(self):
        self.cursor.endOfLine()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class GotoLine(AbstractAction):
    def act(self):
        if self.command.cpCount() == None:
            self.cursor.endOfBuffer()
            self.cursor.beginningOfLine()
        else:
            position = self.command.cpCount(), 1
            self.cursor.position(*position)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Insert(AbstractAction):
    def act(self):
        self.command.next()
        return "insert", self.actionManager.action("insert", "inserting")

class InsertBeforeLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        self.command.next()
        return "insert", self.actionManager.action("insert", "inserting")

class Left(AbstractAction):
    def act(self):
        self.cursor.left(self.command.cpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutBefore(AbstractAction):
    def act(self):
        count = self.command.cpCount()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        if linewise:
            for i in range(count):
                self.buffer.insertLines(self.cursor.y, string)
        else:
            for i in range(count):
                self.buffer.insert(self.cursor.position(), string)
            self.cursor.right(count * len(string) - 1)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutAfter(AbstractAction):
    def act(self):
        count = self.command.cpCount()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        if linewise:
            for i in range(count):
                self.buffer.insertLines(self.cursor.y + 1, string)
            self.cursor.down()
        else:
            if self.buffer.lengthOfLine(self.cursor.y) > 0:
                for i in range(count):
                    position = (self.cursor.y, self.cursor.x + 1)
                    self.buffer.insert(position, string)
                self.cursor.right(count * len(string))
            else:
                return self.actionManager.action("normal", "P").act()

        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Right(AbstractAction):
    def act(self):
        self.cursor.right(self.command.cpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Up(AbstractAction):
    def act(self):
        self.cursor.up(self.command.cpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Yank(AbstractPendingAction):
    def call(self, range):
        string = self.buffer.copyRange(*range)
        self.registerManager.unshift(string)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class YankLines(AbstractAction):
    def act(self):
        count = self.command.cpCount()
        if not count: count = 1
        y, x = self.cursor.position()
        string = self.buffer.copyLines(y, count)
        self.registerManager.unshift(string, True)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")


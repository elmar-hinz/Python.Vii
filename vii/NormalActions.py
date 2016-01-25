from .AbstractAction import AbstractAction
from .AbstractAction import AbstractPendingAction
from .Logger import *
from .Range import Range, Position
from .Cursor import CursorException as CursorException

class Idle(AbstractAction):
    def act(self, dummyCallback = None):
        """ dummy callback required when used as Null
        action from operartor pending mode. """
        operator = self.command.lpOperator()
        return self.actionManager.action("normal", operator).act()

class Append(AbstractAction):
    def act(self):
        self.cursor.appendInLine()
        return "insert", self.actionManager.action("insert", "inserting")

class AppendToLine(AbstractAction):
    def act(self):
        self.cursor.endOfLine()
        self.cursor.appendInLine()
        return "insert", self.actionManager.action("insert", "inserting")

class BeginningOfLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Change(AbstractPendingAction):
    def call(self, range):
        self.buffer.delete(range)
        return "insert", self.actionManager.action("insert", "inserting")

class Delete(AbstractPendingAction):
    def call(self, range):
        debug("Delete")
        debug(range)
        self.buffer.delete(range)
        if range.isLines(): self.cursor.beginningOfLine()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Down(AbstractAction):
    def act(self):
        self.cursor.down(self.command.lpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class EndOfLine(AbstractAction):
    def act(self):
        count = self.command.lpCount()
        self.cursor.endOfLine(count)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class GotoLine(AbstractAction):
    def act(self):
        if self.command.lpCount() == None:
            self.cursor.endOfBuffer()
            self.cursor.beginningOfLine()
        else:
            position = Position(self.command.lpCount(), 1)
            try: self.cursor.position(position)
            except CursorException: pass
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Insert(AbstractAction):
    def act(self):
        return "insert", self.actionManager.action("insert", "inserting")

class InsertBeforeLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        return "insert", self.actionManager.action("insert", "inserting")

class Left(AbstractAction):
    def act(self):
        self.cursor.left(self.command.lpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutBefore(AbstractAction):
    def act(self):
        count = self.command.lpCount()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        if linewise:
            position = Position(self.cursor.y, 1)
            for i in range(count): self.buffer.insert(position, string)
            self.cursor.position(position)
        else:
            for i in range(count):
                self.buffer.insert(self.cursor.position(), string)
            self.cursor.left()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutAfter(AbstractAction):
    def act(self):
        count = self.command.lpCount()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        if linewise:
            position = Position(self.cursor.y + 1, 1)
            for i in range(count): self.buffer.insert(position, string)
            self.cursor.position(position)
        else:
            if self.buffer.lengthOfLine(self.cursor.y) > 1:
                for i in range(count):
                    position = Position(self.cursor.y, self.cursor.x + 1)
                    self.buffer.insert(position, string)
                self.cursor.right(count * len(string))
            else:
                return self.actionManager.action("normal", "P").act()

        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Right(AbstractAction):
    def act(self):
        self.cursor.right(self.command.lpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Up(AbstractAction):
    def act(self):
        self.cursor.up(self.command.lpCount())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Yank(AbstractPendingAction):
    def call(self, range):
        string = self.buffer.copy(range)
        debug(string)
        self.registerManager.unshift(string)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class YankLines(AbstractAction):
    def act(self):
        count = self.command.lpCount()
        if not count: count = 1
        y = self.cursor.y
        string = self.buffer.copy(Range(y, y + count - 1))
        self.registerManager.unshift(string, True)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")



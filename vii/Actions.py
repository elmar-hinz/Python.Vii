from .AbstractAction import AbstractAction
from .AbstractAction import AbstractPendingAction
from .Logger import *
from .Range import Range, Position
from .Cursor import CursorException

class Idle(AbstractAction):
    def act(self, callback = None):
        """ dummy callback required when used as Null
        action from operartor pending mode. """
        operator = self.command.lpOperator()
        return self.actionManager.action("normal", operator).act()

class Append(AbstractAction):
    def act(self, callback = None):
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
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            range = self.motions.down(factor).linewise()
            return callback.call(range)
        else:
            self.cursor.down(factor)
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

class Inserting(AbstractAction):
    def act(self):
        self.step(self.command.lpInsert())
        return ("insert", self)

    def step(self, token):
        if not "startPosition" in dir(self): self.start()
        if False: pass
        elif token == chr(127): self.backspace()
        else: self.insert(token)

    def start(self):
        self.startPosition = self.cursor.position()

    def finish(self):
        super().finish()
        self.cursor.left()

    def insert(self, char):
        if self.buffer.isEmpty():
            self.buffer.insert(Position(1,1), "\n")
            self.cursor.position(Position(1,1))
        y,x = self.cursor.position().toPosition()
        self.buffer.insert(self.cursor.position(), char)

    def backspace(self):
        y = self.cursor.y
        x = self.cursor.x - 1
        startY, startX = self.startPosition.toPosition()
        if (y > startY or x >= startX) and x > 0:
            self.buffer.delete(Position(y, x))

class InsertBeforeLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        return "insert", self.actionManager.action("insert", "inserting")

class Left(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            stop = self.motions.left().toPositions()[1]
            start = self.motions.left(factor).toPositions()[1]
            self.cursor.left(factor)
            return callback.call(Range(start, stop))
        else:
            self.cursor.left(factor)
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
            string = count * string
            if self.buffer.isEmpty():
                position = Position(1,1)
            elif self.buffer.lengthOfLine(self.cursor.y) > 2:
                position = Position(self.cursor.y, self.cursor.x + 1)
            else:
                position = self.cursor.position()
            self.buffer.insert(position, string)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Right(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            range = self.motions.right(factor -1)
            return callback.call(range)
        else:
            self.cursor.right(factor)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class Up(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            range = self.motions.up(factor).linewise()
            return callback.call(range)
        else:
            self.cursor.up(factor)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class Yank(AbstractPendingAction):
    def call(self, range):
        string = self.buffer.copy(range)
        self.registerManager.unshift(string, range.isLines())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class YankLines(AbstractAction):
    def act(self, callback = None):
        if callback:
            if self.command.previous().operator == "y":
                factor = self.command.multiplyAll()
                return self.redirect("Y", factor)
            else:
                return skipToIdle()
        else:
            count = self.command.lpCount()
            if not count: count = 1
            y = self.cursor.y
            string = self.buffer.copy(Range(y, y + count - 1))
            self.registerManager.unshift(string, True)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")



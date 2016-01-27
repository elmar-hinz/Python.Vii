from .AbstractAction import AbstractAction
from .AbstractAction import AbstractPendingAction
from .Logger import *
from .Range import Range, Position
from .Cursor import CursorException

class Idle(AbstractAction):
    def act(self, callback = None):
        operator = self.command.lpOperator()
        return self.actionManager.action("normal", operator).act()

class Append(AbstractAction):
    def act(self, callback = None):
        self.cursor.appendInLine()
        return "insert", self.actionManager.action("insert", "inserting")

class AppendToLine(AbstractAction):
    " No count "
    def act(self):
        self.cursor.endOfLine()
        self.cursor.appendInLine()
        return "insert", self.actionManager.action("insert", "inserting")

class BeginningOfLine(AbstractAction):
    " No count "
    def act(self, callback = None):
        motion = self.motions.beginningOfLine()
        if callback:
            start = motion.lastPosition()
            stop = self.motions.left().lastPosition()
            return callback.call(Range(start, stop))
        else:
            self.cursor.move(motion)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class Change(AbstractPendingAction):
    def call(self, range):
        self.buffer.delete(range)
        if range.isLines():
            y = range.upperY()
            self.buffer.insert(Position(y, 1), "\n")
            self.cursor.gotoPositionRelaxed(Position(y, 1))
        else:
            self.cursor.gotoPositionRelaxed(range.upperPosition())
        return "insert", self.actionManager.action("insert", "inserting")

class Delete(AbstractPendingAction):
    def call(self, range):
        self.buffer.delete(range)
        if range.isLines():
            y = range.upperY()
            self.cursor.gotoPositionRelaxed(Position(y, 1))
        else:
            self.cursor.gotoPositionRelaxed(range.upperPosition())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Down(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            motion = self.motions.down(factor).linewise()
            return callback.call(motion)
        else:
            self.cursor.down(factor)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class EndOfLine(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        motion = self.motions.endOfLine(factor)
        if callback:
            return callback.call(motion)
        else:
            self.cursor.move(motion)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class GotoLine(AbstractAction):
    def act(self):
        if self.command.lpCount() == None:
            self.cursor.endOfBuffer()
            self.cursor.beginningOfLine()
        else:
            position = Position(self.command.lpCount(), 1)
            self.cursor.gotoPositionStrict(position)
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
            start = self.motions.left(factor).lastPosition()
            stop = self.motions.left().lastPosition()
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
        string *= count
        if linewise:
            position = Position(self.cursor.y, 1)
            self.buffer.insert(position, string)
            self.cursor.position(position)
        else:
            if self.buffer.isEmpty():
                self.buffer.fill("\n")
                self.cursor.beginningOfBuffer()
            self.buffer.insert(self.cursor.position(), string)
            self.cursor.left()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutAfter(AbstractAction):
    def act(self):
        count = self.command.lpCount()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        string *= count
        if linewise:
            position = Position(self.cursor.y + 1, 1)
            self.buffer.insert(position, string)
            self.cursor.position(position)
        else:
            if self.buffer.isEmpty():
                self.buffer.fill("\n")
                self.cursor.beginningOfBuffer()
            elif self.buffer.lengthOfLine(self.cursor.y) > 1:
                self.cursor.appendInLine()
            self.buffer.insert(self.cursor.position(), string)
            self.cursor.right(len(string))
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
        if range.isLines():
            y = range.upperY()
            x = self.cursor.x
            self.cursor.gotoPositionStrict(Position(y, x))
        else:
            self.cursor.gotoPositionStrict(range.upperPosition())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class YankLines(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            if self.command.previous().operator == "y":
                return self.redirect("Y", factor)
            else:
                return skipToIdle()
        else:
            yRange = self.motions.down(factor - 1).linewise()
            string = self.buffer.copy(yRange)
            self.registerManager.unshift(string, True)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")


from .AbstractAction import *
from .Logger import *
from .Range import Range, Position
from .Buffer import LastLinebreakLostExecption

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

class BackWord(AbstractWord):
    backwards = True
    pattern = r'\w+'

class BackWORD(AbstractWord):
    backwards = True
    pattern = r'\S+'

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

class ChangeLines(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            if not self.command.previous().operator == "c":
                return self.skipToIdle()
            range = self.motions.down(factor - 1).linewise()
        else:
            range = self.motions.endOfLine(factor)
        return self.actionManager.action("normal", "c").call(range)

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

class DeleteCharacters(AbstractAction):
    def act(self):
        factor = self.command.multiplyAll()
        range = self.motions.right(factor - 1)
        self.buffer.delete(range)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class DeleteCharactersBefore(AbstractAction):
    def act(self):
        factor = self.command.multiplyAll()
        if self.cursor.x > 1:
            start = self.motions.left(factor).lastPosition()
            stop = self.motions.left().lastPosition()
            self.buffer.delete(Range(start, stop))
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class DeleteLines(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            if not self.command.previous().operator == "d":
                return self.skipToIdle()
            range = self.motions.down(factor - 1).linewise()
        else:
            range = self.motions.endOfLine(factor)
        return self.actionManager.action("normal", "d").call(range)

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

class EndOfWord(AbstractWord):
    backwards = False
    pattern = r'\w\W'

class EndOfWORD(AbstractWord):
    backwards = False
    pattern = r'\S\s'

class FindInLine(AbstractFindInLine):
    backwards = False

class FindInLineBackwards(AbstractFindInLine):
    backwards = True

class GotoLine(AbstractAction):
    def act(self, callback = None):
        if self.command.hasNoCounts():
            y = self.buffer.countOfLines()
        else:
            y = self.command.multiplyAll()
        motion = self.motions.gotoPositionStrict(Position(y,1))
        if callback:
            return callback.call(motion.linewise())
        else:
            self.cursor.move(motion)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class GCommand(AbstractAction):
    def __init__(self):
        self.callback = None

    def act(self, callback = None):
        """
        If act() is called from a pending action that
        action is given as callback. While collecting the
        g command components this callback is stored into
        **self.callback**. When the command is ready and
        finally called, that callback is submitted with
        act(). It's call() method is called directly,
        hence no call() command needed here. """
        mode = self.dispatcher.currentMode
        if mode == "gPending":
            operator = self.command.lpOperator()
            if self.callback:
                return self.actionManager.action(mode, operator).act(self.callback)
            else:
                return self.actionManager.action(mode, operator).act()
        else:
            if callback: self.callback = callback
            self.dispatcher.extend()
            return "gPending", self

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
        self.buffer.insert(self.cursor.position(), char)

    def backspace(self):
        y = self.cursor.y
        x = self.cursor.x - 1
        startY, startX = self.startPosition.toPositionTuple()
        if (y > startY or x >= startX) and x > 0:
            self.buffer.delete(Position(y, x))

class InsertBeforeLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        return "insert", self.actionManager.action("insert", "inserting")

class JoinLinesWithAdjustments(AbstractAction):
    def act(self):
        factor = self.command.multiplyAll()
        y = self.cursor.y
        for i in range(factor):
            if y < self.buffer.countOfLines():
                joinPosition = Position(y, self.buffer.lengthOfLine(y))
                # firstLine without newline
                firstLine = self.buffer.copy(Range(y,y))
                firstLine = firstLine[:-1]
                firstLengthTrimmed = len(firstLine.rstrip())
                if (len(firstLine) - firstLengthTrimmed) > 0: joint = ""
                else: joint = " "
                # last line left stripped
                lastLine = self.buffer.copy(Range(y+1, y+1)).lstrip()
                if lastLine == "": lastLine = "\n"
                self.buffer.delete(Range(y, y+1))
                joined = firstLine + joint  + lastLine
                self.buffer.insert(Position(y, 1), joined)
                self.cursor.gotoPositionStrict(joinPosition)
        return "normal", self.actionManager.action("normal", "idle")

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

class OpenLineAbove(AbstractAction):
    def act(self):
        self.buffer.insert(Position(self.cursor.y, 1), "\n")
        self.cursor.up()
        return "insert", self.actionManager.action("insert", "inserting")

class OpenLineBelow(AbstractAction):
    def act(self):
        self.buffer.insert(Position(self.cursor.y + 1, 1), "\n")
        self.cursor.down()
        return "insert", self.actionManager.action("insert", "inserting")

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

class ReplaceCharacters(AbstractAction):
    def act(self):
        mode = self.dispatcher.currentMode
        if mode == "pending":
            position = self.cursor.position()
            factor = self.command.multiplyAll()
            range = self.motions.right(factor - 1)
            self.buffer.delete(range)
            self.buffer.insert(position,
                factor*self.command.lpOperator())
            self.cursor.move(position)
            self.cursor.right(factor - 1)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")
        else:
            self.dispatcher.extend()
            return "pending", self

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

class Word(AbstractWord):
    backwards = False
    pattern = r'\w+'

class WORD(AbstractWord):
    backwards = False
    pattern = r'\S+'

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
        if callback and not self.command.previous().operator == "y":
            return self.skipToIdle()
        else:
            factor = self.command.multiplyAll()
            yRange = self.motions.down(factor - 1).linewise()
            return self.actionManager.action("normal", "y").call(yRange)


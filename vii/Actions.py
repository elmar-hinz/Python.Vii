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
            return callback.call(motion.exclusive())
        else:
            return self.moveAndFinshToIdle(motion)

class BackWord(AbstractWord):
    backwards = True
    pattern = r'\w+'

class BackWORD(AbstractWord):
    backwards = True
    pattern = r'\S+'

class Change(AbstractPendingAction):
    def call(self, motion):
        if motion:
            self.buffer.delete(motion)
            if motion.isLines():
                y = motion.upperY()
                self.buffer.insert(Position(y, 1), "\n")
                self.cursor.gotoPositionRelaxed(Position(y, 1))
            else:
                self.cursor.gotoPositionRelaxed(motion.upperPosition())
        return "insert", self.actionManager.action("insert", "inserting")

class ChangeLines(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            """ cc acts linewise """
            if not self.command.previous().operator == "c":
                return self.skipToIdle()
            motion = self.motions.down(factor - 1).limitVertical().linewise()
        else:
            """ C acts from current position """
            motion = self.motions.endOfLine(factor)
        return self.actionManager.action("normal", "c").call(motion)

class Delete(AbstractPendingAction):
    def call(self, motion):
        if motion:
            self.buffer.delete(motion)
            if motion.isLines():
                y = motion.upperY()
                self.cursor.gotoPositionStrict(Position(y, 1))
            else:
                self.cursor.gotoPositionStrict(motion.upperPosition())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class DeleteCharacters(AbstractAction):
    def act(self):
        factor = self.command.multiplyAll()
        motion = self.motions.right(factor - 1).forceLimits()
        self.buffer.delete(motion)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class DeleteCharactersBefore(AbstractAction):
    def act(self):
        factor = self.command.multiplyAll()
        motion = self.motions.left(factor)
        motion = motion.forceLimits()
        motion = motion.exclusive()
        self.buffer.delete(motion)
        return self.moveAndFinshToIdle(motion)

class DeleteLines(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        if callback:
            """ dd acts linewise """
            if not self.command.previous().operator == "d":
                return self.skipToIdle()
            motion = self.motions.down(factor - 1).limitVertical().linewise()
        else:
            """ D acts from current position """
            motion = self.motions.endOfLine(factor).forceLimits()
        return self.actionManager.action("normal", "d").call(motion)

class Down(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        motion = self.motions.down(factor).limitVertical()
        if callback:
            return callback.call(motion.linewise())
        else:
            return self.moveAndFinshToIdle(motion)

class EndOfLine(AbstractAction):
    def act(self, callback = None):
        factor = self.command.multiplyAll()
        motion = self.motions.endOfLine(factor)
        motion = motion.forceLimits()
        if callback:
            return callback.call(motion)
        else:
            return self.moveAndFinshToIdle(motion)

class EndOfWord(AbstractWord):
    backwards = False
    pattern = r'\w\W'
    matchEmptyLines = False
    exclusive = False

class EndOfWORD(AbstractWord):
    backwards = False
    pattern = r'\S\s'
    matchEmptyLines = False
    exclusive = False

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
        motion = self.motions.makeMotion(Position(y,1))
        motion = motion.limitVertical()
        if callback:
            return callback.call(motion.linewise())
        else:
            return self.moveAndFinshToIdle(motion)

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
        motion = self.motions.left(factor)
        motion = motion.forceLimits()
        motion = motion.exclusive()
        if callback:
            return callback.call(motion)
        else:
            return self.moveAndFinshToIdle(motion)

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
            y = self.cursor.y
            position = Position(y if y else 1, 1)
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
        motion = self.motions.right(factor)
        if callback:
            motion = motion.forceLimits(1)
            return callback.call(motion.exclusive())
        else:
            motion = motion.forceLimits()
            return self.moveAndFinshToIdle(motion)

class ReplaceCharacters(AbstractAction):
    def act(self):
        mode = self.dispatcher.currentMode
        if mode == "pending":
            position = self.cursor.position()
            factor = self.command.multiplyAll()
            motion = self.motions.right(factor - 1)
            motion = motion.forceLimits()
            self.buffer.delete(motion)
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
        motion = self.motions.up(factor).limitVertical()
        if callback:
            return callback.call(motion.linewise())
        else:
            return self.moveAndFinshToIdle(motion)

class Word(AbstractWord):
    backwards = False
    pattern = r'\w+'
    changeAlternativePattern = r'\w\W'

class WORD(AbstractWord):
    backwards = False
    pattern = r'\S+'
    changeAlternativePattern = r'\S\s'

class Yank(AbstractPendingAction):
    def call(self, motion):
        if not motion:
            string = ""
            self.registerManager.unshift(string)
        else:
            string = self.buffer.copy(motion)
            self.registerManager.unshift(string, motion.isLines())
            if motion.isLines():
                y = motion.upperY()
                x = self.cursor.x
                self.cursor.gotoPositionStrict(Position(y, x))
            else:
                self.cursor.gotoPositionStrict(motion.upperPosition())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class YankLines(AbstractAction):
    def act(self, callback = None):
        if callback and not self.command.previous().operator == "y":
            """ yy and Y work both linewise """
            return self.skipToIdle()
        else:
            factor = self.command.multiplyAll()
            yRange = self.motions.down(factor - 1).limitVertical().linewise()
            return self.actionManager.action("normal", "y").call(yRange)


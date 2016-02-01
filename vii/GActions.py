from .AbstractAction import *
from .Range import Range, Position
from .Logger import debug

class GotoTop(AbstractAction):
    def act(self, callback = None):
        y = self.command.multiplyAll()
        motion = self.motions.gotoPositionStrict(Position(y,1))
        if callback:
            return callback.call(motion.linewise())
        else:
            self.cursor.move(motion)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

class JoinLinesWithoutAdjustments(AbstractAction):
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
                lastLine = self.buffer.copy(Range(y+1, y+1))
                self.buffer.delete(Range(y, y+1))
                joined = firstLine + lastLine
                self.buffer.insert(Position(y, 1), joined)
                self.cursor.gotoPositionStrict(joinPosition)
        return "normal", self.actionManager.action("normal", "idle")

class EndOfWordBackwards(AbstractWord):
    backwards = True
    pattern = r"\w\W"
    exclusive = False

class EndOfWORDBackwards(AbstractWord):
    backwards = True
    pattern = r"\S\s"
    exclusive = False



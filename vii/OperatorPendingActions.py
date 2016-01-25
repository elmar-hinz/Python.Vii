from .AbstractAction import AbstractAction
from .Range import Range
from .Logger import debug

class Down(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        range = self.motions.down(factor).linewise()
        return callback.call(range)

class Left(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        stop = self.motions.left().toPositions()[1]
        start = self.motions.left(factor).toPositions()[1]
        self.cursor.left(factor)
        return callback.call(Range(start, stop))

class Right(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        range = self.motions.right(factor -1)
        return callback.call(range)

class Up(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        range = self.motions.up(factor).linewise()
        return callback.call(range)

class YankLines(AbstractAction):
    def act(self, callback):
        if self.command.previous().operator == "y":
            factor = self.command.multiplyAll()
            return self.redirect("Y", factor)
        else:
            return skipToIdle()



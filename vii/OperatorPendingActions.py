from .AbstractAction import AbstractAction
from .Range import Range
from .Logger import debug

class Down(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        range = self.ranges.down(factor)
        return callback.call(Range(range))

class Left(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        stop = self.ranges.left()
        start = self.ranges.left(factor)
        self.cursor.left(factor)
        return callback.call(Range(start, stop))

class Right(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        start = self.cursor.position()
        stop = self.ranges.right(factor - 1)
        return callback.call(Range(start, stop))

class Up(AbstractAction):
    def act(self, callback):
        factor = self.command.multiplyAll()
        range = self.ranges.up(factor)
        return callback.call(Range(range))

class YankLines(AbstractAction):
    def act(self, callback):
        if self.command.previous().operator == "y":
            factor = self.command.multiplyAll()
            return self.redirect("Y", factor)
        else:
            return skipToIdle()



from .AbstractAction import AbstractAction
from .Logger import *

class Left(AbstractAction):
    def act(self, callback):
        factor = self.multiplyCounts()
        stop = self.ranges.left()
        start = self.ranges.left(factor)
        self.cursor.left(factor)
        return callback.call((start, stop))

class Right(AbstractAction):
    def act(self, callback):
        factor = self.multiplyCounts()
        start = self.cursor.position()
        stop = self.ranges.right(factor - 1)
        return callback.call((start, stop))

class YankLines(AbstractAction):
    def act(self, callback):
        if self.dispatcher.operator() == "y":
            factor = self.multiplyCounts()
            command = self.dispatcher.command()
            command['count'] = factor
            command['operator'] = "Y"
            command['count2'] = 0
            command['operator2'] = ""
            return self.actionManager.action("normal", "idle").act()

        else:
            self.finish()
            return self.actionManager.action("normal", "idle").act()



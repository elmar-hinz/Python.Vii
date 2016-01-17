from .AbstractAction import AbstractAction
from .Logger import *

class AbstractPendingAction(AbstractAction):
    def act(self):
        if not self.dispatcher.operatorPendingReady():
            return "operatorPending", self
        else:
            operator = self.dispatcher.operatorPendingOperator()
            action = self.actionManager.action("operatorPending", operator)
            if action == None:
                self.dispatcher.reset()
                return self.actionManager.action("normal", "idle")
            else:
                return action.act(self)

    def call(self, range): pass

class Yank(AbstractPendingAction):
    def call(self, range):
        string = self.buffer.copyRange(*range)
        self.registerManager.unshift(string)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Delete(AbstractPendingAction):
    def call(self, range):
        self.buffer.deleteRange(*range)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Change(AbstractPendingAction):
    def call(self, range):
        self.buffer.deleteRange(*range)
        return "insert", self.actionManager.action("insert", "inserting")

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



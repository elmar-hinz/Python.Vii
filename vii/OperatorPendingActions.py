from .AbstractAction import AbstractAction
from .Logger import *

class AbstractPendingAction(AbstractAction):
    def act(self):
        if not self.dispatcher.operatorPendingReady():
            return "operatorPending", self
        else:
            operator = self.dispatcher.operatorPendingOperator()
            return self.actionManager.action("operatorPending", operator).act(self)

    def call(self, range): pass

class Yank(AbstractPendingAction):
    def call(self, range):
        string = self.buffer.copyRange(*range)
        debug(str(string))
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
        factor = (self.dispatcher.count() *
            self.dispatcher.operatorPendingCount())
        stop = self.move.left()
        start = self.move.left(factor)
        self.cursor.position(*self.move.left(factor))
        return callback.call((start, stop))

class Right(AbstractAction):

    def act(self, callback):
        factor = (self.dispatcher.count() *
            self.dispatcher.operatorPendingCount())
        start = self.cursor.position()
        stop = self.move.right(factor - 1)
        return callback.call((start, stop))


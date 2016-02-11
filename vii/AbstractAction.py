from .Logger import *
from .Range import *

class AbstractAction:
    def act(self, callback = None): pass

    def finish(self):
        self.dispatcher.logHistory()
        self.dispatcher.reset()

    def XXXredirect(self, operator, count = None):
            self.dispatcher.reset()
            part = self.dispatcher.currentCommand.last()
            part.operator = operator
            if count:
                part.numeral = str(count)
                part.count = count
            part.ready = True
            return self.actionManager.action("normal", "idle").act()

    def skipToIdle(self):
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

    def moveAndFinshToIdle(self, motion):
        if motion: motion = motion.forceLimits()
        self.cursor.move(motion)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class AbstractPendingAction(AbstractAction):
    def act(self, callback = None):
        mode = self.dispatcher.currentMode
        if mode == "operatorPending":
            operator = self.command.lpOperator()
            return self.actionManager.action(mode, operator).act(self)
        else:
            self.dispatcher.extend()
            return "operatorPending", self

    def call(self, range): pass

class AbstractFindInLine(AbstractAction):
    backwards = False

    def __init__(self):
        self.callback = None

    def act(self, callback = None):
        mode = self.dispatcher.currentMode
        if mode == "pending":
            pattern = self.command.lpOperator()
            factor = self.command.multiplyAll()
            if self.backwards:
                motion = self.motions.beginningOfLine()
            else:
                motion = self.motions.endOfLine()
            motion = motion.forceLimits()
            motion = self.motions.find(
               pattern = pattern,
               range = motion, step = factor,
               backwards = self.backwards,
               matchEmptyLines = False,
               matchRangeBorders = False)
            if self.callback:
                return self.callback.call(motion)
            else:
                self.cursor.move(motion)
                self.finish()
                return "normal", self.actionManager.action("normal", "idle")
        else:
            if callback: self.callback = callback
            self.dispatcher.extend()
            self.dispatcher.forceTokenToString = True
            return "pending", self

class AbstractWord(AbstractAction):
    backwards = False
    pattern = None
    exclusive = True
    matchEmptyLines = True
    matchRangeBorders = True

    def __init__(self):
        self.callback = None

    def act(self, callback = None):
        if(callback and
            self.command.previous().operator == "c"):
            self.pattern = self.changeAlternativePattern
            self.exclusive = False
        factor = self.command.multiplyAll()
        start = self.cursor.position()
        if self.backwards: stop = Position(1,0)
        else: stop = self.buffer.lastPosition()
        range = Range(start, stop)
        motion = self.motions.find(
           pattern = self.pattern,
           range = range, step = factor,
           backwards = self.backwards,
           matchEmptyLines = self.matchEmptyLines,
           matchRangeBorders = self.matchRangeBorders)
        motion = motion.forceLimits()
        if not motion.isTwoPositions():
            return self.skipToIdle()
        elif callback:
            if self.exclusive: motion = motion.exclusive()
            return callback.call(motion)
        else:
            return self.moveAndFinshToIdle(motion)


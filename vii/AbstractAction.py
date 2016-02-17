from .Logger import *
from .Range import *

class AbstractAction:
    def act(self, callback = None): pass

    def finish(self):
        self.dispatcher.logHistory()
        self.dispatcher.reset()

    def skipToIdle(self):
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

    def moveAndFinshToIdle(self, motion):
        if motion: motion = motion.forceLimits()
        self.cursor.move(motion)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

    def deleteAndRegister(self, motion):
        string = self.buffer.delete(motion)
        self.registerManager.shift(string, motion.isLines())

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
    pattern = "%s"
    repeat = None

    def __init__(self):
        self.callback = None

    def act(self, callback = None):
        mode = self.dispatcher.currentMode
        if mode == "pending" or self.repeat:
            factor = self.command.multiplyAll()
            if not self.repeat:
                backwards = self.backwards
                token = self.command.lpOperator()
                self.globalVariables.set("findInLineBackwards", backwards)
                self.globalVariables.set("findInLineToken", token)
            else:
                backwards = self.globalVariables.get("findInLineBackwards")
                token = self.globalVariables.get("findInLineToken")
                if self.repeat == "inversed": backwards = not backwards
            if backwards:
                range = self.motions.beginningOfLine()
            else:
                range = self.motions.endOfLine()
            range = range.forceLimits()
            motion = self.motions.find(
               pattern = (self.pattern % token),
               range = range, step = factor,
               backwards = backwards,
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


from .Logger import *

class AbstractAction:
    def act(self, callback = None): pass

    def finish(self):
        self.dispatcher.logHistory()
        self.dispatcher.reset()

    def redirect(self, operator, count = None):
            self.dispatcher.reset()
            part = self.dispatcher.currentCommand.last()
            part.operator = "Y"
            if count:
                part.numeral = str(count)
                part.count = count
            part.ready = True
            return self.actionManager.action("normal", "idle").act()

    def skipToIdle(self):
        self.dispatcher.reset()
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
            token = self.command.lpOperator()
            factor = self.command.multiplyAll()
            if self.backwards:
                range = self.motions.beginningOfLine()
            else:
                range = self.motions.endOfLine()
            motion = self.motions.find(token, range,
                    factor, self.backwards)
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

    def __init__(self):
        self.callback = None

    def act(self, callback = None):
            factor = self.command.multiplyAll()
            if self.backwards: range = self.motions.beginningOfBuffer()
            else: range = self.motions.endOfBuffer()
            motion = self.motions.find(
               pattern = self.pattern,
               range = range, step = factor,
               backwards = self.backwards,
               matchEmptyLines = True)
            if callback:
                debug(motion)
                if self.exclusive: motion = motion.exclusive()
                debug(motion)
                return callback.call(motion)
            else:
                self.cursor.move(motion)
                self.finish()
                return "normal", self.actionManager.action("normal", "idle")


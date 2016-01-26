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

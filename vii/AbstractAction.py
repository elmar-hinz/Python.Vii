class AbstractAction:

    def act(self): pass

    def range(self): pass

    def finish(self):
        self.dispatcher.logHistory()
        self.dispatcher.reset()

    def multiplyCounts(self):
        count1 = self.dispatcher.count()
        count2 = self.dispatcher.operatorPendingCount()
        if not count1: count1 = 1
        if not count2: count2 = 1
        return count1 * count2

class AbstractPendingAction(AbstractAction):

    def act(self):
        if not self.dispatcher.operatorPendingReady():
            return "operatorPending", self
        else:
            operator = self.dispatcher.operatorPendingOperator()
            return self.actionManager.action("operatorPending", operator).act(self)

    def call(self, range): pass

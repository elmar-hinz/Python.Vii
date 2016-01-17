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



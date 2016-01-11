class AbstractAction:

    def act(self): pass

    def finish(self):
        self.dispatcher.logHistory()
        self.dispatcher.reset()

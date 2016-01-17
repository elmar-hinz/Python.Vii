class AbstractAction:

    def act(self): pass

    def range(self): pass

    def finish(self):
        self.dispatcher.logHistory()
        self.dispatcher.reset()

    @staticmethod
    def nextX(position):
        return (position[0], position[1] + 1)

    @staticmethod
    def nextY(position):
        return (position[0] + 1)

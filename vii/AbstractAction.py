from .BufferRanges import BufferRanges

class AbstractAction:

    def __init__(self, dispatcher, windowManager, actionManager):
        self.actionManager = actionManager
        self.dispatcher = dispatcher
        self.windowManager = windowManager
        window = windowManager.window
        self.buffer = windowManager.buffer
        self.cursor = windowManager.cursor
        self.move = BufferRanges(self.buffer, self.cursor)

    def act(self): pass

    def finish(self): pass

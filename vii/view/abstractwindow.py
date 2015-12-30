import curses
from ..signals import slot

class AbstractWindow:

    buffer = None

    def __init__(self, parentWindow, modelId):
        window = curses.newwin(*self.layout(parentWindow))
        window.refresh()
        self.window = window
        slot(modelId, self)

    def draw(self):
        self.window.clear()
        self.window.addstr(str(self.buffer))
        self.window.refresh()

    def receive(self, modelId, model):
        self.draw()


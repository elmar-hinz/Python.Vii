import curses
from ..Signals import slot

class AbstractWindow:

    buffer = None
    cursor = None

    def __init__(self, parentWindow):
        window = curses.newwin(*self.layout(parentWindow))
        window.refresh()
        self.window = window
        slot("bufferUpdate", self)

    def draw(self):
        self.window.clear()
        self.window.addstr(str(self.buffer))
        self.window.refresh()

    def receive(self, signal, sender, *args):
        self.draw()


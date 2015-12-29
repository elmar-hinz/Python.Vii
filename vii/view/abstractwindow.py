import curses

class AbstractWindow:

    buffer = None

    def __init__(self, parentWindow):
        window = curses.newwin(*self.layout(parentWindow))
        window.refresh()
        self.window = window

    def draw(self):
        self.window.clear()
        self.window.addstr(str(self.buffer))
        self.window.refresh()


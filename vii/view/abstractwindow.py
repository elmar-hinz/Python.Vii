import curses

class AbstractWindow:

    def __init__(self, parentWindow):
        window = curses.newwin(*self.layout(parentWindow))
        window.refresh()
        self.window = window

    def draw(self, text):
        self.window.clear()
        self.window.addstr(text)
        self.window.refresh()


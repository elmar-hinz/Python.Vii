import curses

class CommandLine:

    def __init__(self, parentWindow):
        height, width = 1, parentWindow.getmaxyx()[1]
        x, y = 0, parentWindow.getmaxyx()[0] - 1
        window = curses.newwin(height, width, y, x)
        window.refresh()
        self.window = window

    def draw(self, text):
        self.window.clear()
        self.window.addstr(text)
        self.window.refresh()


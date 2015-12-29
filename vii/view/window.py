from .abstractwindow import AbstractWindow
from .renderer import render

class Window(AbstractWindow):

    def __init__(self, parentWindow):
        super().__init__(parentWindow)

    def layout(self, parentWindow):
        height, width = parentWindow.getmaxyx()
        x, y = 0, 0
        return (height - 1, width, y, x)

    def draw(self):
        self.window.clear()
        self.window.addstr(render(self.buffer))
        self.window.refresh()


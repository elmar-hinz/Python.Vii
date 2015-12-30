from .abstractwindow import AbstractWindow
from .renderer import render
import curses
from ..logger import *

class Window(AbstractWindow):

    buffer = None

    def __init__(self, parentWindow):
        super().__init__(parentWindow)

    def layout(self, parentWindow):
        height, width = parentWindow.getmaxyx()
        x, y = 0, 0
        return (height - 1, width, y, x)

    def draw(self):
        self.window.clear()
        self.window.addstr(render(self.buffer))
        self.move()
        self.window.refresh()

    def move(self):
        debug("move %s %s" % self.buffer.cursor.position())
        self.window.move(*self.buffer.cursor.position())


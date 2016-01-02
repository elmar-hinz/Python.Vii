from ..Setup import numberBarWidth
from .AbstractWindow import AbstractWindow
from .Renderer import render
import curses
from ..Signals import slot
from ..Logger import *

class Window(AbstractWindow):

    buffer = None

    def __init__(self, parentWindow):
        super().__init__(parentWindow)
        slot("cursorMoved", self)

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
        y, x = self.cursor.position()
        debug("move %s %s" % (y, x))
        x += numberBarWidth
        self.window.move(y, x)


from .Buffer import Buffer
from .Motions import Motions
from .Cursor import Cursor
from .Search import Search
from .view.Window import Window, WindowLines
from .Logger import debug
import curses

class Port:

    def dimensions(self):
        return self.screen.getmaxyx()

    def height(self):
        return self.dimensions()[0]

    def width(self):
        return self.dimensions()[1]

    def clear(self):
        self.screen.clear()

    def draw(self, string):
        self.screen.clear()
        self.screen.addstr(string[:-1])
        self.screen.refresh()

    def move(self, y, x):
        self.screen.move(y-1, x-1)
        self.screen.refresh()

class WindowManager:

    def currentWindow(self):
        return self.window

    def commandLineWindow(self):
        return self.commandLine

    def createPort(self, parentScreen):
        height, width = parentScreen.getmaxyx()
        layout = (height - 1, width, 0, 0)
        port = Port()
        port.screen = curses.newwin(*layout)
        return port

    def createCommandPort(self, parentScreen):
        height, width = parentScreen.getmaxyx()
        y = height - 1
        layout = (1, width, y, 0)
        port = Port()
        port.screen = curses.newwin(*layout)
        return port

    def createWindow(self, port):
        """ TODO: multiple windows """
        """ TODO: dynamic relation between buffer and windows """
        """ The cursor shall belong to the window buffer relation, so that the same buffer can display different cursor positions in different windows. This window buffer relation shall contain more status informations. """
        cursor = Cursor()
        buffer = Buffer()
        motions = Motions()
        window = Window()
        window.port = port
        window.lines = WindowLines()
        # window.lines.splitLines("", 1)
        cursor.buffer = buffer
        cursor.motions = motions
        motions.buffer = buffer
        motions.cursor = cursor
        motions.search = Search()
        motions.search.buffer = buffer
        window.cursor = cursor
        window.buffer = buffer
        window.motions = motions
        return window


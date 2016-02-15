from .Buffer import Buffer
from .Motions import Motions
from .Cursor import Cursor
from .Search import Search
from .view.Window import Window, Port, WindowLines

class WindowManager:

    def __init__(self, parentScreen, view):
        self.parentScreen = parentScreen
        self.view = view
        self.createWindow()
        self.window.draw()

    def createWindow(self):
        """ TODO: multiple windows """
        """ TODO: dynamic relation between buffer and windows """
        self.cursor = Cursor()
        self.buffer = Buffer()
        self.motions = Motions()
        self.port = Port(self.parentScreen)
        self.window = Window()
        self.window.port = self.port
        self.window.lines = WindowLines()
        self.window.lines.splitLines("", 1)
        self.cursor.buffer = self.buffer
        self.cursor.motions = self.motions
        self.motions.buffer = self.buffer
        self.motions.cursor = self.cursor
        self.motions.search = Search()
        self.motions.search.buffer = self.buffer
        self.window.cursor = self.cursor
        self.window.buffer = self.buffer


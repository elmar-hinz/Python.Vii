from .Buffer import Buffer
from .Motions import Motions
from .Cursor import Cursor
from .view.Window import Window

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
        self.buffer.insertLines(1,"")
        self.motions = Motions()
        self.window = Window(self.parentScreen)
        self.cursor.buffer = self.buffer
        self.cursor.motions = self.motions
        self.motions.buffer = self.buffer
        self.motions.cursor = self.cursor
        self.window.cursor = self.cursor
        self.window.buffer = self.buffer



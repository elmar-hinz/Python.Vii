from .Buffer import Buffer
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
        buffer = Buffer()
        buffer.insertLines(0,"")
        self.window = Window(self.parentScreen)
        self.window.buffer = buffer
        cursor = Cursor(buffer)
        self.window.cursor = cursor



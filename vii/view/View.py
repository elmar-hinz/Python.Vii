from .CommandLine import CommandLine
from .Window import Window
from ..Logger import debug

class View:
    def __init__(self, root):
        self.root = root
        root.refresh()
        # self.commandLine = CommandLine(root, "commandLine")

    def createWindow(self, buffer, cursor):
        """ TODO: add to windowlist """
        self.window = Window(self.root)
        self.window.buffer = buffer
        self.window.cursor = cursor


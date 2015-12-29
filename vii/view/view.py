from .commandline import CommandLine
from .window import Window
from ..logger import debug

class View:
    def __init__(self, root):
        self.root = root
        root.refresh()
        self.commandLine = CommandLine(root)

    def createWindow(self, buffer):
        """ TODO: add to windowlist """
        self.window = Window(self.root)
        self.window.buffer = buffer



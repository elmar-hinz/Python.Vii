from .commandline import CommandLine
from .window import Window

class View:
    def __init__(self, root):
        self.root = root
        root.refresh()
        self.window = Window(root)
        self.commandLine = CommandLine(root)


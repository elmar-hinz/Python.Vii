from .CommandLine import CommandLine
from .Window import Window, Port
from ..Logger import debug

class View:

    def __init__(self, root):
        self.root = root
        root.refresh()
        # self.commandLine = CommandLine(root, "commandLine")



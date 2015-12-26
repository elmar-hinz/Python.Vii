from .commandline import CommandLine

class View:
    def __init__(self, root):
        self.root = root
        root.refresh()
        self.commandLine = CommandLine(root)



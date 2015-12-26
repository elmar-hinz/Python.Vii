from .commandmode import CommandMode

class Controller:
    def __init__(self, model, view):
        self.model, self.view = model, view
        self.commandMode = CommandMode(self)
        self.currentMode = self.commandMode

    def loop(self):
        self.view.root.nodelay(0)
        while True:
            key = self.view.root.getch()
            self.currentMode = self.currentMode.handleKey(key)


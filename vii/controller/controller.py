from .commandmode import CommandMode
from .editmode import EditMode
from ..logger import logger

class Controller:

    def __init__(self, model, view):
        self.model, self.view = model, view
        self.wireUp()
        self.commandMode = CommandMode(self)
        self.editMode = EditMode(self)
        self.currentMode = self.commandMode

    def wireUp(self):
        self.view.commandLine.setBuffer(self.model.commandLine)

    def loop(self):
        self.view.root.nodelay(0)
        while True:
            key = self.view.root.getch()
            self.currentMode = self.currentMode.handleKey(key)


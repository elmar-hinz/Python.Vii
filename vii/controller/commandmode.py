from .abstractmode import AbstractMode
from ..logger import logger

class CommandMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.model = controller.model.commandLine
        self.view = controller.view.commandLine

    def handleKey(self, key):
        super().handleKey(key)
        if key == 127: return self.backspace()
        if key == 10: return self.submit()
        else: return self.append(key)

    def append(self, key):
        self.model.append(chr(key))
        self.view.draw()
        return self.controller.commandMode

    def backspace(self):
        self.model.delete(self.model.length() - 1)
        self.view.draw()
        return self.controller.commandMode

    def submit(self):
        self.model.clear()
        self.view.draw()
        return self.controller.commandMode



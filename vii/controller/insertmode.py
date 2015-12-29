from .abstractmode import AbstractMode
from ..logger import *

class InsertMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.view = controller.view.window
        self.buffer = controller.model.buffer
        self.line = self.buffer[-1]

    def handleKey(self, key):
        super().handleKey(key)
        if key == 127: return self.backspace()
        if key == 27: return self.controller.editMode
        if key == 10: return self.newline()
        else: return self.append(key)

    def newline(self):
        self.line = self.buffer.createMember()
        self.buffer.append(self.line)
        self.view.draw()
        return self.controller.insertMode



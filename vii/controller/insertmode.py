from .abstractmode import AbstractMode
from ..logger import *

class InsertMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.window = controller.view.window
        self.buffer = controller.model.buffer
        self.cursor = self.buffer.cursor

    def currentLine(self):
        return self.buffer[self.cursor.y]

    def handleKey(self, key):
        super().handleKey(key)
        if key == 10: return self.newline()
        if key == 27: return self.controller.editMode
        if key == 127: return self.backspace()
        else: return self.append(key)

    def append(self, key):
        debug("Apppend: %s" % key)
        line = self.currentLine()
        line.append(chr(key))
        x = self.buffer.cursor.x + 1
        self.buffer.cursor.position(x = x)
        self.window.draw()
        return self.controller.currentMode

    def backspace(self):
        line = self.currentLine()
        line.delete(line.length() - 1)
        x = self.buffer.cursor.x - 1
        self.buffer.cursor.position(x = x)
        self.window.draw()
        return self.controller.currentMode

    def newline(self):
        line = self.currentLine()
        line = self.buffer.createMember()
        self.buffer.append(line)
        y = self.buffer.cursor.y + 1
        self.buffer.cursor.position(y, 0)
        self.window.draw()
        return self.controller.insertMode



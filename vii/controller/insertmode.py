from .abstractmode import AbstractMode
from ..logger import *

class InsertMode(AbstractMode):

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.view.window
        self.buffer = parent.model.buffer
        self.cursor = self.buffer.cursor

    def currentLine(self):
        return self.buffer[self.cursor.y]

    def handleKey(self, key):
        super().handleKey(key)
        if key == 10: self.newline()
        elif key == 127: self.backspace()
        else: self.insert(key)

    def insert(self, key):
        debug("Insert: %s" % key)
        x = self.buffer.cursor.x
        line = self.currentLine()
        line.insert(x, chr(key))
        self.buffer.cursor.position(x = x + 1)

    def backspace(self):
        line = self.currentLine()
        line.delete(line.length() - 1)
        x = self.buffer.cursor.x - 1
        self.buffer.cursor.position(x = x)

    def newline(self):
        line = self.currentLine()
        line = self.buffer.createMember()
        self.buffer.append(line)
        y = self.buffer.cursor.y + 1
        self.buffer.cursor.position(y, 0)


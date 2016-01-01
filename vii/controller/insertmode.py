from .abstractmode import AbstractMode
from ..logger import *

class InsertMode(AbstractMode):

    startPosition = None

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent.view.window
        self.buffer = self.window.buffer
        self.cursor = self.window.cursor

    def handleKey(self, key):
        super().handleKey(key)
        if not self.startPosition: self.start()
        if key == 10: self.newline()
        elif key == 27: self.finish()
        elif key == 127: self.backspace()
        else: self.insert(key)

    def start(self):
        self.startPosition = self.cursor.position()

    def finish(self):
        self.startPosition = None

    def insert(self, key):
        debug("Insert: %s" % key)
        x = self.cursor.x
        self.line().insert(x, chr(key))
        self.cursor.position(x = x + 1)

    def backspace(self):
        y = self.cursor.y
        x = self.cursor.x - 1
        if y > self.startPosition[0] or x >= self.startPosition[1]:
            self.line().delete(x)
            self.cursor.position(x = x)

    def newline(self):
        line = self.buffer.createMember()
        self.buffer.append(line)
        y = self.cursor.y + 1
        self.cursor.position(y, 0)

    def line(self):
        return self.buffer[self.cursor.y]


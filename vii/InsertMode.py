from .AbstractMode import AbstractMode
from .Logger import *

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
        if False: pass
        elif key == 10: self.newline()
        elif key == 27: self.finish()
        elif key == 127: self.backspace()
        else: self.insert(key)

    def start(self):
        self.startPosition = self.cursor.position()

    def finish(self):
        self.startPosition = None

    def insert(self, key):
        debug("Insert: %s" % key)
        y,x = self.cursor.position()
        self.buffer.insert((y,x), chr(key))
        self.cursor.position(x = x + 1)

    def backspace(self):
        y = self.cursor.y
        x = self.cursor.x - 1
        if y > self.startPosition[0] or x >= self.startPosition[1]:
            if x >= 0:
                self.buffer.deleteRange((y,x), (y,x))
                self.cursor.position(x = x)

    def newline(self):
        debug("Insert: Newline")
        y,x = self.cursor.position()
        self.buffer.insert((y,x), '\n')
        y = self.cursor.y + 1
        self.cursor.position(y, 0)


from .Logger import *
from .AbstractAction import AbstractAction

class Inserting(AbstractAction):

    def act(self):
        self.step(self.dispatcher.token())
        return ("insert", self)

    def step(self, token):
        if not "startPosition" in dir(self): self.start()
        if False: pass
        elif token == chr(10): self.newline()
        elif token == chr(127): self.backspace()
        else: self.insert(token)

    def start(self):
        self.startPosition = self.cursor.position()

    def finish(self):
        super().finish()
        self.cursor.position(*self.ranges.left())

    def insert(self, char):
        debug("Insert: %s" % char)
        y,x = self.cursor.position()
        debug("Position: %s, %s" % (y, x))
        self.buffer.insert((y,x), char)
        self.cursor.position(x = x + 1)

    def backspace(self):
        debug("Insert: Backspace")
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


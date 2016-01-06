from .Logger import *
from .AbstractAction import AbstractAction

class Inserting(AbstractAction):

    def act(self):
        debug("Inserting")
        if not self.dispatcher.ready():
            self.step(self.dispatcher.character())
        else:
            debug(self.dispatcher.operator())
            raise Exception
        return ("insert", self)

    ##########################

    startPosition = None

    # def __init__(self, windowManager, commandCatcher):
    #     self.window = windowManager.window
    #     self.buffer = self.window.buffer
    #     self.cursor = self.window.cursor

    def step(self, char):
        if not self.startPosition: self.start()
        if False: pass
        elif char == chr(10): self.newline()
        elif char == chr(127): self.backspace()
        else: self.insert(char)

    def start(self):
        self.startPosition = self.cursor.position()

    def finish(self):
        self.startPosition = None

    def insert(self, char):
        debug("Insert: %s" % char)
        y,x = self.cursor.position()
        self.buffer.insert((y,x), char)
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


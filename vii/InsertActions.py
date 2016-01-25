from .Logger import *
from .AbstractAction import AbstractAction
from .Range import Range, Position

class Inserting(AbstractAction):

    def act(self):
        self.step(self.command.lpInsert())
        return ("insert", self)

    def step(self, token):
        if not "startPosition" in dir(self): self.start()
        if False: pass
        elif token == chr(127): self.backspace()
        else: self.insert(token)

    def start(self):
        self.startPosition = self.cursor.position()

    def finish(self):
        super().finish()
        self.cursor.left()

    def insert(self, char):
        if self.buffer.isEmpty():
            self.buffer.insert(Position(1,1), "\n")
            self.cursor.position(Position(1,1))
        y,x = self.cursor.position().toPosition()
        self.buffer.insert(self.cursor.position(), char)

    def backspace(self):
        y = self.cursor.y
        x = self.cursor.x - 1
        startY, startX = self.startPosition.toPosition()
        if (y > startY or x >= startX) and x > 0:
            self.buffer.delete(Position(y, x))


from .abstractlist import AbstractList
from .line import Line
from ..signals import signal
from ..logger import *

class Buffer(AbstractList):

    memberClass = Line
    cursor = None

    def __init__(self, id, text = None):
        super().__init__(id)
        self.parse(text)
        """ assert at least one empty line """
        if len(self) == 0:
            self.append(self.createMember())
        signal(self.id, self)

    def parse(self, text):
        try:
            for line in text.splitlines():
                self.append(self.createMember(line))
        except AttributeError: pass
        signal(self.id, self)

    def createMember(self, text = ""):
        return Line(text)


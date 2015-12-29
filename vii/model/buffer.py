from .abstractlist import AbstractList
from .line import Line
from ..logger import *

class Buffer(AbstractList):

    memberClass = Line
    cursor = None

    def __init__(self, text = None):
        super().__init__()
        self.parse(text)
        """ assert at least one empty line """
        if len(self) == 0:
            self.append(self.createMember())

    def parse(self, text):
        try:
            for line in text.splitlines():
                self.append(self.createMember(line))
        except AttributeError: pass

    def createMember(self, text = ""):
        return Line(text)


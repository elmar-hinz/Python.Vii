from .abstractlist import AbstractList
from .line import Line
from ..signals import signal
from ..logger import *

class Buffer(AbstractList):

    memberClass = Line

    def __init__(self, text = None):
        super().__init__()
        self.parse(text)
        """ assert at least one empty line """
        if len(self) == 0:
            self.append(self.createMember())
        signal("bufferUpdate", self)

    def parse(self, text):
        try:
            for line in text.splitlines():
                self.append(self.createMember(line))
        except AttributeError: pass
        signal("bufferUpdate", self)

    def createMember(self, text = ""):
        return Line(self, text)

    def getLine(self, nr):
        return self[nr]

    def insert(self, nr, subject):
        list = self.toList(subject)
        self[nr:nr] = list
        signal("bufferUpdate", self)
        signal("verticalInsert", self, nr, len(list))

    def delete(self, nr, count = 1):
        super().delete(nr, count)
        signal("verticalDelete", self, nr, count)




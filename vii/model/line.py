from .abstractlist import AbstractList
from ..signals import signal
from ..logger import *

class Line(AbstractList):

    memberClass = str

    def __init__(self, buffer, text = ""):
        super().__init__()
        self.buffer = buffer
        self.parse(text)

    def __str__(self):
        return ''.join(self)

    def parse(self, text):
        for char in text: self.append(char)

    def createMember(self, char = ' '):
        if not len(char) == 1: raise Exception
        return char

    def insert(self, nr, subject):
        list = self.toList(subject)
        self[nr:nr] = list
        signal("bufferUpdate", self)
        signal("horizontalInsert", self.buffer,
            nr, len(list))

    def delete(self, nr, count = 1):
        super().delete(nr, count)
        signal("horizontalDelete", self.buffer,
            nr, count)


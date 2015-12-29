from .abstractlist import AbstractList

from ..logger import *

class Line(AbstractList):

    memberClass = str

    def __init__(self, text = ""):
        super().__init__()
        self.parse(text)

    def __str__(self):
        return ''.join(self)

    def parse(self, text):
        for char in text: self.append(char)

    def createMember(self, char = ' '):
        if not len(char) == 1: raise Exception
        return char


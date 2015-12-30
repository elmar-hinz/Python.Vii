from .line import Line
from .buffer import Buffer
from ..logger import *

class Model:
    def __init__(self):
        self.commandLine = Line()

    def createBuffer(self, cursor):
        """ TODO add to bufferlist """
        self.buffer = Buffer()
        self.buffer.cursor = cursor
        cursor.buffer = self.buffer
        return self.buffer

from ..buffer import Buffer
from ..logger import *

class Model:
    def __init__(self):
        # self.commandLine = Line()
        pass

    def createBuffer(self):
        """ TODO add to bufferlist """
        self.buffer = Buffer()
        self.buffer.insertLines(0,"")
        return self.buffer

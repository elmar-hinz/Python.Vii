from .Buffer import Buffer
from .Logger import *

class Model:
    def __init__(self):
        # self.commandLine = Line()
        pass

    def createBuffer(self):
        """ TODO add to bufferlist """
        self.buffer = Buffer()
        self.buffer.insertLines(0,"")
        return self.buffer

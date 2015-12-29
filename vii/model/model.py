from .line import Line
from .buffer import Buffer
from ..logger import *

class Model:
    def __init__(self):
        self.commandLine = Line()
        self.buffer = Buffer()
        debug(self.buffer.length())

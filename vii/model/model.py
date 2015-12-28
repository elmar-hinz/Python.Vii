from .line import Line
from .buffer import Buffer

class Model:
    def __init__(self):
        self.commandLine = Line()
        self.buffer = Buffer()



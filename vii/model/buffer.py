from .abstractlist import AbstractList
from .line import Line

class Buffer(AbstractList):
    pass

    @staticmethod
    def createElement():
        return Line()



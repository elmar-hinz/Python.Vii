from .abstractlist import AbstractList

class Line(AbstractList):
    pass

    def __str__(self):
        return ''.join(self.list)


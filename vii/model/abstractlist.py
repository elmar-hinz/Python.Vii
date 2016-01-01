from ..logger import *
from ..signals import signal

class AbstractList(list):

    """ class of list members """
    memberClass = None

    def __init__(self):
        list.__init__(self)
        signal("bufferUpdate", self)

    def append(self, subject):
        self.extend(self.toList(subject))
        signal("bufferUpdate", self)

    def createMember(self):
        return self.memberClass()

    def delete(self, nr, count = 1):
        self[nr:nr+count] = []
        signal("bufferUpdate", self)

    def insert(self, nr, subject):
        self[nr:nr] = self.toList(subject)
        signal("bufferUpdate", self)

    def length(self):
        return len(self)

    def replace(self, nr, subject):
        list = self.toList(subject)
        self[nr:nr+len(list)] = list
        signal("bufferUpdate", self)

    def __str__(self):
        return "\n".join(str(e) for e in self)

    def toList(self, subject):
        if not subject.__class__ == self.memberClass: return subject
        else: return [subject]


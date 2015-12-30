from ..logger import *
from ..signals import signal

class AbstractList(list):

    """ class of list members """
    memberClass = None
    id = None

    def __init__(self, id = None):
        list.__init__(self)
        self.id = id
        if self.id: signal(self.id, self)

    def append(self, subject):
        self.extend(self.__list(subject))
        if self.id: signal(self.id, self)

    def createMember(self):
        return self.memberClass()

    def delete(self, nr, count = 1):
        self[nr:nr+count] = []
        if self.id: signal(self.id, self)

    def insert(self, nr, subject):
        self[nr:nr] = self.__list(subject)
        if self.id: signal(self.id, self)

    def length(self):
        return len(self)

    def replace(self, nr, subject):
        list = self.__list(subject)
        self[nr:nr+len(list)] = list
        if self.id: signal(self.id, self)

    def __str__(self):
        return "\n".join(str(e) for e in self)

    def __list(self, subject):
        if not subject.__class__ == self.memberClass: return subject
        else: return [subject]


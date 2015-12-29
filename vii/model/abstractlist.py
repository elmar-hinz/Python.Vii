from ..logger import *

class AbstractList(list):

    """ class of list members """
    memberClass = None

    def __init__(self):
        list.__init__(self)

    def append(self, subject):
        self.extend(self.__list(subject))

    def createMember(self):
        return self.memberClass()

    def delete(self, nr, count = 1):
        self[nr:nr+count] = []


    def insert(self, nr, subject):
        self[nr:nr] = self.__list(subject)

    def length(self):
        return len(self)

    def replace(self, nr, subject):
        list = self.__list(subject)
        self[nr:nr+len(list)] = list

    def __str__(self):
        return "\n".join(str(e) for e in self)

    def __list(self, subject):
        if not subject.__class__ == self.memberClass: return subject
        else: return [subject]



class AbstractList:

    def __init__(self):
        self.clear()

    def asList(self):
        return self.list

    def append(self, subject):
        self.list.extend(self.__list(subject))

    def clear(self):
        self.list = []

    def delete(self, nr, count = 1):
        self.list[nr:nr+count] = []

    def insert(self, nr, subject):
        insert = self.__list(subject)
        begin, end = self.list[:nr], self.list[nr:]
        self.list = begin + insert + end

    def length(self):
        return len(self.list)

    def read(self, nr, count = None):
        if count: return self.list[nr:nr+count]
        else: return self.list[nr]

    def replace(self, nr, subject):
        list = self.__list(subject)
        self.list[nr:nr+len(list)] = list

    def __str__(self):
        return "\n".join(str(e) for e in self.list)

    @staticmethod
    def __list(subject):
        if '__iter__' in dir(subject): return subject
        else: return [subject]


from .Logger import *
class Part:

    def __init__(self):
        self.numeral = ""
        self.operator = ""
        self.inserts = []
        self.register = None
        self.count = None
        self.ready = False

    def appendToNumeral(self,  tokoen):
        self.numeral += tokoen

    def appendToInserts(self, token):
        self.inserts.append(token)

    def numeralToCount(self):
        if len(self.numeral) > 0:
            self.count = int(self.numeral)

    def insert(self):
        return self.inserts[-1]

class Command:

    def __init__(self):
        self.parts = []

    def extend(self):
        self.parts.append(Part())

    def part(self, nr):
        return self.parts[nr]

    def previous(self):
        return self.parts[-2]

    def last(self):
        return self.parts[-1]

    def multiplyAll(self):
        result = 1
        for i in range(len(self.parts)):
            count = self.parts[i].count
            count = count if count else 1
            result *= count
        return result

    """ Shortcuts to the last part """

    def lpReady(self):
        return self.last().ready

    def lpRegister(self):
        return self.last().register

    def lpOperator(self):
        return self.last().operator

    def lpCount(self):
        return self.last().count

    def lpInserts(self):
        return self.last().inserts

    def lpInsert(self):
        return self.last().insert()




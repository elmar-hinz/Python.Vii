class Part:

    def __init__(self):
        self.numeral = ""
        self.operator = ""
        self.inserts = ""
        self.register = None
        self.count = None
        self.token = None
        self.ready = False

    def appendToNumeral(self,  tokoen):
        self.numeral += tokoen

    def appendToInserts(self, token):
        self.inserts += token

    def numeralToCount(self):
        if len(self.numeral) > 0:
            self.count = int(self.numeral)

class Command:

    def __init__(self):
        self.parts = []
        self.position = 0

    def extend(self):
        self.parts.append(Part())

    def part(self, nr):
        return self.parts[nr]

    def current(self):
        return self.parts[self.position]

    def last(self):
        return self.parts[-1]

    def next(self):
        self.position += 1

    def rewind(self):
        self.position = 0

    def multiplyAll(self):
        result = 1
        for i in range(len(self.parts)):
            result *= self.parts[i].count
        return result

    """ Shortcuts to current part """

    def cpReady(self):
        return self.current().ready

    def cpRegister(self):
        return self.current().register

    def cpOperator(self):
        return self.current().operator

    def cpCount(self):
        return self.current().count

    def cpInserts(self):
        return self.current().inserts

    def cpToken(self):
        return self.current().token




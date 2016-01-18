class Part:

    def __init__(self):
        self.register = None
        self.numeral = ""
        self.count = None
        self.token = None

    def appendToNumeral(self, digit):
        self.numeral += digit

    def numeralToCount(self):
        self.count = int(self.numeral)


class Command:

    def __init__(self):
        self.parts = []
        self.position = 0

    def extend(self):
        self.parts.append(Part())

    def last(self):
        return self.parts[-1]

    def getPart(self, nr):
        return self.parts[nr]

    def nextPart(self):
        part = self.parts[self.position]
        self.position += 1
        return part

    def rewind(self):
        self.position = 0

    def multiplyAll(self):
        result = 1
        for i in range(len(self.parts)):
            result *= self.parts[i].count
        return result


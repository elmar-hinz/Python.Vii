
class Variables:

    def __init__(self):
        self.storage = dict()

    def set(self, name, value):
        self.storage[name] = value

    def get(self, name):
        return self.storage[name]


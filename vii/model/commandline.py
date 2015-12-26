
class CommandLine:

    def __init__(self):
        self.clear()

    def append(self, string):
        self.text += string

    def clear(self):
        self.text = ""

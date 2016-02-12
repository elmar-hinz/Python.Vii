class RegisterManager:

    def __init__(self):
        self.numbered = 10 * [tuple(["", False])]
        self.named = dict()
        self.unnamed = "0"

    def shift(self, string, linewise = False):
        value = tuple([string, linewise])
        self.unnamed = '1'
        self.numbered[1:10] = [value] + self.numbered[1:9]

    def store(self, name, string, linewise = False):
        if name == '_': return
        if name == '"':
            return self.store(0, string, linewise)
        name = str(name)
        value = tuple([string, linewise])
        if name.isdigit():
            self.numbered[int(name)] = value
        else:
            self.named[name] = value
        self.unnamed = name

    def fetch(self, name):
        name = str(name)
        if name == '"':
            return self.fetch(self.unnamed)
        if name.isdigit():
            try: return self.numbered[int(name)]
            except IndexError: return ("", False)
        else:
            try: return self.named[name]
            except KeyError: return ("", False)


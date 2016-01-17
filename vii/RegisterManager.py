class RegisterManager:

    def __init__(self):
        self.yankRegister = []

    def unshift(self, string, linewise = False):
        t = tuple([string, linewise])
        self.yankRegister = [t] + self.yankRegister[:9]

    def read(self, nr = 0):
        try:
            return self.yankRegister[nr]
        except IndexError:
            return ("", False)


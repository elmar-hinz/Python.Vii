import sys
from .Logger import debug

class CommandCatcher:

    def __init__(self, commandMap):
        self.map = self.parseMap(commandMap)
        self.reset()

    def parseMap(self, text):
        map = dict()
        for line in text.strip().splitlines():
            try:
                k, v = tuple(i.strip() for i in line.split(":"))
                map[k] = v
            except:
                pass
        return map

    def ready(self, key):
        if self.parts == None:
            self.parts = {'count': "0", 'operator': "", 'action': None}
        if chr(key).isdigit():
            self.parts['count'] += chr(key)
            return False
        else:
            self.parts['count'] = int(self.parts['count'])
            self.parts['operator'] += chr(key)
            try:
                self.parts['action'] = self.map[self.parts['operator']]
            except KeyError:
                pass
            return True

    def count(self):
        return self.parts['count']

    def action(self):
        return self.parts['action']

    def operator(self):
        return self.parts['operator']

    def reset(self):
        self.parts = None


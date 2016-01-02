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
            self.parts = {'count': "0", 'operator': ""}
        if chr(key).isdigit():
            self.parts['count'] += chr(key)
            return False
        else:
            self.parts['count'] = int(self.parts['count'])
            self.parts['operator'] += chr(key)
            return True

    def count(self):
        return self.parts['count']

    def command(self):
        try:
            return self.map[self.parts['operator']]
        except KeyError:
            return None

    def reset(self):
        self.parts = None


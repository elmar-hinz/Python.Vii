
class ActionManager:

    def __init__(self):
        self.dispatcher = None
        self.windowManager =  None
        self.actionMaps = dict()
        self.actionModules = dict()

    def addModule(self, mode, module):
        self.actionModules[mode] = module

    def addMap(self, mode, map):
        self.actionMaps[mode] = self.parseMap(map)

    def action(self, mode, operator):
        action = self.actionMaps[mode][operator]
        action = action.capitalize()
        module = self.actionModules[mode]
        Action = getattr(module, action)
        return Action(self.dispatcher, self.windowManager)

    def parseMap(self, text):
        map = dict()
        for line in text.strip().splitlines():
            try:
                k, v = tuple(i.strip() for i in line.split(":"))
                map[k] = v
            except:
                pass
        return map


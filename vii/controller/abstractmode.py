from .. logger import logger

class AbstractMode:

    def __init__(self, controller):
        self.controller = controller

    def handleKey(self, key):
        logger.debug(key)

    def append(self, key):
        self.line.append(chr(key))
        self.view.draw()
        return self.controller.currentMode

    def backspace(self):
        self.line.delete(self.line.length() - 1)
        self.view.draw()
        return self.controller.currentMode

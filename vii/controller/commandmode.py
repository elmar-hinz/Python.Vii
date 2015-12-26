from ..logger import logger
import sys

class CommandMode:

    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model.commandLine
        self.view = controller.view.commandLine

    def handleKey(self, key):
        logger.debug(key)
        if key == 127: return self.backspace()
        if key == 10: return self.submit()
        else: return self.append(key)

    def append(self, key):
        self.model.append(chr(key))
        self.view.draw(self.model.text)
        return self.controller.commandMode

    def backspace(self):
        self.model.text = self.model.text[:-1]
        self.view.draw(self.model.text)
        return self.controller.commandMode

    def submit(self):
        self.model.text = ""
        self.view.draw(self.model.text)
        return self.controller.commandMode



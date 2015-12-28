from .abstractmode import AbstractMode

class CommandMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.line = controller.model.commandLine
        self.view = controller.view.commandLine

    def handleKey(self, key):
        super().handleKey(key)
        if key == 127: return self.backspace()
        if key == 10: return self.submit()
        else: return self.append(key)

    def submit(self):
        self.line.clear()
        self.view.draw()
        return self.controller.commandMode



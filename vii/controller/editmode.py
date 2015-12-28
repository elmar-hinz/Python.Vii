from .abstractmode import AbstractMode

class EditMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)
        self.view = controller.view.window
        self.model = controller.model.buffer
        self.line = self.model.createElement()
        self.model.append(self.line)

    def handleKey(self, key):
        super().handleKey(key)
        if key == 27: return self.controller.commandMode
        return self.controller.editMode



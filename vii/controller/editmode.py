
from .abstractmode import AbstractMode
from ..logger import logger

class EditMode(AbstractMode):

    def __init__(self, controller):
        super().__init__(controller)

    def handleKey(self, key):
        super().handleKey(key)
        return self.controller.editMode


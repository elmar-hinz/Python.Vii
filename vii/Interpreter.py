from .Logger import debug
from .App import QuitException

class Interpreter:
    def interpret(self, string):
        parts = string.split()
        action = self.actionManager.action(parts[0], parts[1:])
        if action: action.act()

class AbstractInterpreterAction:
    def act(self): pass

class EditAction(AbstractInterpreterAction):
    def act(self):
        try:
            address = self.command[0]
            self.window.buffer.read(address)
        except IndexError:
            pass

class WriteAction(AbstractInterpreterAction):
    def act(self):
        try:
            address = self.command[0]
            self.window.buffer.write(address)
        except IndexError:
            self.window.buffer.write()

class QuitAction(AbstractInterpreterAction):
    def act(self):
        debug("quit")
        raise(QuitException)

class InterpreterActionManager:
    def action(self, operator, command):
        if operator == "write": Action = WriteAction
        elif operator == "edit": Action = EditAction
        elif operator == "quit": Action = QuitAction
        else: return None
        action = Action()
        action.command = command
        action.window = self.window
        return action


from .Logger import debug

class Interpreter:

    def interpret(self, string):
        parts = string.split()
        action = self.actionManager.action(parts[0], parts[1:])
        if action: action.act()

class AbstractInterpreterAction:

    def act(self): pass

class WriteAction(AbstractInterpreterAction):

    def act(self):
        debug("write", self.command[0])

class QuitAction(AbstractInterpreterAction):

    def act(self):
        debug("quit")

class InterpreterActionManager:

    def action(self, operator, command):
        if operator == "write": Action = WriteAction
        elif operator == "edit": Action = EditAction
        elif operator == "quit": Action = QuitAction
        else: return None
        action = Action()
        action.command = command
        return action


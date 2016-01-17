from .AbstractAction import AbstractAction
from .Logger import *

class Idle(AbstractAction):
    def act(self):
        if self.dispatcher.ready():
            operator = self.dispatcher.operator()
            action = self.actionManager.action("normal", operator)
            if action == None:
                self.dispatcher.reset()
                return "normal", self
            else:
                return action.act()
        else:
            return "normal", self

class Append(AbstractAction):
    def act(self):
        self.cursor.appendInLine()
        return "insert", self.actionManager.action("insert", "inserting")

class AppendToLine(AbstractAction):
    def act(self):
        self.cursor.endOfLine()
        self.cursor.appendInLine()
        return "insert", self.actionManager.action("insert", "inserting")

class BeginningOfLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Change(AbstractAction):
    def act(self):
        return self.actionManager.action("operatorPending", "change").act()

class Delete(AbstractAction):
    def act(self):
        return self.actionManager.action("operatorPending", "delete").act()

class Down(AbstractAction):
    def act(self):
        self.cursor.down(self.dispatcher.count())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class EndOfLine(AbstractAction):
    def act(self):
        self.cursor.endOfLine()
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class GotoLine(AbstractAction):
    def act(self):
        if self.dispatcher.count() == None:
            self.cursor.endOfBuffer()
            self.cursor.beginningOfLine()
        else:
            position = self.dispatcher.count(), 0
            self.cursor.position(*position)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Insert(AbstractAction):
    def act(self):
        return "insert", self.actionManager.action("insert", "inserting")

class InsertBeforeLine(AbstractAction):
    def act(self):
        self.cursor.beginningOfLine()
        return "insert", self.actionManager.action("insert", "inserting")

class Left(AbstractAction):
    def act(self):
        self.cursor.left(self.dispatcher.count())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutBefore(AbstractAction):
    def act(self):
        count = self.dispatcher.count()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        if linewise:
            for i in range(count):
                self.buffer.insertLines(self.cursor.y, string)
        else:
            for i in range(count):
                self.buffer.insert(self.cursor.position(), string)
            self.cursor.right(count * len(string) - 1)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class PutAfter(AbstractAction):
    def act(self):
        count = self.dispatcher.count()
        if count == None: count = 1
        string, linewise = self.registerManager.read()
        if linewise:
            for i in range(count):
                self.buffer.insertLines(self.cursor.y + 1, string)
            self.cursor.down()
        else:
            for i in range(count):
                position = (self.cursor.y, self.cursor.x + 1)
                self.buffer.insert(position, string)
            self.cursor.right(count * len(string))
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Right(AbstractAction):
    def act(self):
        self.cursor.right(self.dispatcher.count())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Up(AbstractAction):
    def act(self):
        self.cursor.up(self.dispatcher.count())
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")

class Yank(AbstractAction):
    def act(self):
        return self.actionManager.action("operatorPending", "yank").act()

class YankLines(AbstractAction):
    def act(self):
        count = self.dispatcher.count()
        if not count: count = 1
        y, x = self.cursor.position()
        string = self.buffer.copyLines(y, count)
        self.registerManager.unshift(string, True)
        self.finish()
        return "normal", self.actionManager.action("normal", "idle")


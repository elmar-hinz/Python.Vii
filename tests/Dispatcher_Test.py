from vii.Dispatcher import Dispatcher, TokenExecption
from vii.Command import Command
from nose.tools import *

class FinshActionSeen(Exception): pass

class Action:
    finishSeen = False
    def finish(self): self.finishSeen = True
    def act(self): return "actSeen"

class ActionManager:
    actionCalled = 0

    def action(self, mode, operator):
        self.actionCalled += 1
        return self.Action

class Dispatcher_Test:
    def setup(self):
        self.fixture = Dispatcher()
        self.actionManager = ActionManager()
        self.action = Action()
        self.actionManager.Action = self.action
        self.fixture.actionManager = self.actionManager

    def test__init__(self):
        fixture = Dispatcher()
        assert fixture.actionManager == None
        assert fixture.currentMode == None
        assert fixture.currentAction == None
        assert fixture.currentCommand == None

    @raises(TokenExecption)
    def test_stepInit_raises_exception_for_int(self):
        self.fixture.stepInit(1)

    def test_stepInit(self):
        assert self.fixture.currentMode == None
        assert self.fixture.currentAction == None
        self.fixture.stepInit("a")
        assert self.fixture.currentMode == "normal"
        assert self.fixture.currentAction == self.action
        command = self.fixture.currentCommand
        assert command.__class__ == Command

    def test_stepCommand_inserts(self):
        self.fixture.reset()
        self.fixture.currentMode = "insert"
        inserts = self.fixture.currentCommand.lpInserts()
        assert inserts == []
        self.fixture.stepCommand("a")
        self.fixture.stepCommand("b")
        assert inserts == ["a", "b"]

    def test_stepCommand_normal(self):
        self.fixture.reset()
        self.fixture.currentMode = "normal"
        self.fixture.stepCommand("1")
        self.fixture.stepCommand("1")
        assert self.fixture.currentCommand.lpReady() == False
        assert self.fixture.currentCommand.lpCount() == 11
        self.fixture.stepCommand("a")
        assert self.fixture.currentCommand.lpReady() == True
        assert self.fixture.currentCommand.lpOperator() == "a"

    def test_stepAction(self):
        pass
        # TODO

    def test_reset(self):
        self.fixture.currentCommand = None
        self.fixture.reset()
        command = self.fixture.currentCommand
        assert command.__class__ == Command
        assert len(command.parts) == 1


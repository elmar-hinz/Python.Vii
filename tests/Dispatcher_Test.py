from vii.Dispatcher import Dispatcher

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
        self.dispatcher = Dispatcher()
        self.actionManager = ActionManager()
        self.action = Action()
        self.actionManager.Action = self.action
        self.dispatcher.actionManager = self.actionManager

    def test__init__(self):
        assert self.dispatcher.windowManager == None
        assert self.dispatcher.currentAction == None
        assert self.dispatcher.parts == None
        assert self.dispatcher.operatorReady == False
        assert self.actionManager.actionCalled == 0

    def test_reset(self):
        self.dispatcher.parts = dict()
        self.dispatcher.reset()
        assert self.dispatcher.parts == None

    def test_stepAction(self):
        assert self.dispatcher.currentAction == None
        self.dispatcher.stepAction(0)
        result = self.dispatcher.currentAction
        assert result == "actSeen"
        assert not self.action.finishSeen
        assert self.actionManager.actionCalled == 1

    def test_stepActionEscape(self):
        self.dispatcher.stepAction(27)
        assert self.action.finishSeen
        assert self.actionManager.actionCalled == 2

    def test_ready_without_count(self):
        self.dispatcher.stepCommand(ord('a'))
        assert self.dispatcher.ready()
        assert self.dispatcher.count() == 1
        assert self.dispatcher.operator() ==  "a"

    def test_ready_with_count(self):
        self.dispatcher.stepCommand(ord('1'))
        self.dispatcher.stepCommand(ord('2'))
        assert not self.dispatcher.ready()
        self.dispatcher.stepCommand(ord('b'))
        assert self.dispatcher.ready()
        assert self.dispatcher.count() == 12
        assert self.dispatcher.operator() ==  "b"

    # def test_ready_with_invalid_command(self):
    #     status = self.dispatcher.ready(ord('z'))
    #     assert self.dispatcher.operator() == 'z'


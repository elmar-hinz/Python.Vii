from vii.Dispatcher import Dispatcher, TokenExecption
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
        self.dispatcher = Dispatcher()
        self.actionManager = ActionManager()
        self.action = Action()
        self.actionManager.Action = self.action
        self.dispatcher.actionManager = self.actionManager

    def test__init__(self):
        assert self.actionManager.actionCalled == 0
        assert self.dispatcher.windowManager == None
        assert self.dispatcher.currentMode == None
        assert self.dispatcher.currentAction == None
        assert self.dispatcher.currentToken == None
        assert self.dispatcher.currentCommand == None
        assert self.dispatcher.newCommand == None
        assert self.dispatcher.operatorReady == False
        assert self.dispatcher.operator2Ready == False

    @raises(TokenExecption)
    def test_stepInit_raises_exception_for_int(self):
        self.dispatcher.stepInit(1)

    def test_stepInit(self):
        assert self.dispatcher.currentMode == None
        assert self.dispatcher.currentAction == None
        self.dispatcher.stepInit("a")
        assert self.dispatcher.currentMode == "normal"
        assert self.dispatcher.currentAction == self.action

    def test_stepCommand_inserts(self):
        self.dispatcher.reset()
        self.dispatcher.currentMode = "insert"
        inserts = self.dispatcher.currentCommand['inserts']
        assert inserts == []
        self.dispatcher.stepCommand("a")
        self.dispatcher.stepCommand("b")
        assert inserts == ["a", "b"]

    def test_stepCommand_normal(self):
        self.dispatcher.reset()
        assert self.dispatcher.ready() == False
        self.dispatcher.currentMode = "normal"
        self.dispatcher.stepCommand("1")
        self.dispatcher.stepCommand("1")
        assert self.dispatcher.ready() == False
        self.dispatcher.stepCommand("a")
        assert self.dispatcher.ready() == True
        assert self.dispatcher.count() == 11
        assert self.dispatcher.operator() == "a"
        expect = {
                "inserts" : [],
                'count': 11,
                'operator': "a",
                'count2': "",
                'operator2': "",
                }
        assert self.dispatcher.command() == expect

    def test_stepCommand_operatorPending(self):
        self.dispatcher.reset()
        assert self.dispatcher.operatorPendingReady() == False
        self.dispatcher.currentMode = "operatorPending"
        self.dispatcher.stepCommand("1")
        self.dispatcher.stepCommand("1")
        assert self.dispatcher.operatorPendingReady() == False
        self.dispatcher.stepCommand("a")
        assert self.dispatcher.operatorPendingReady() == True
        expect = {
                "inserts" : [],
                'count': "",
                'operator': "",
                'count2': 11,
                'operator2': "a",
                }
        assert self.dispatcher.command() == expect

    def test_reset(self):
        self.dispatcher.operatorReady = True
        self.dispatcher.currentCommand = dict()
        self.dispatcher.reset()
        expect = {
                "inserts" : [],
                'count': "",
                'operator': "",
                'count2': "",
                'operator2': "",
                }
        assert self.dispatcher.currentCommand == expect
        self.dispatcher.operatorReady = False


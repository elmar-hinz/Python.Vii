from nose.tools import *
from nose.plugins.skip import SkipTest
from vii.NormalActions import *
import vii.NormalActions

""" Mocks """

class AbstractAction: pass

class Dispatcher:

    def __init__(self):
        self._ready = False

    def ready(self):
        return self._ready

    def operator(self):
        return "operator"

class ActionMangaer:

    def __init__(self):
        self._action = None
        self.wanted = (None, None)

    def action(self, mode, operator):
        self.wanted = (mode, operator)
        return (mode, self._action)

class Action:

    def __init__(self):
        self.actSeen = False

    def act(self):
        self.actSeen = True

class Cursor:

    def __init__(self):
        self.gettingSeen = False
        self.initialPosition = (1, 1)
        self.finalPosition = (1, 1)

    def position(self, y = None, x = None):
        if y == None or x == None:
            self.gettingSeen = True
            return self.initialPosition
        else:
            self.finalPosition = (y, x)


""" Tests """

class Test_Idle:

    def setup(self):
        Idle.__bases__ = (AbstractAction,)
        self.action = Idle()
        self.action.dispatcher = Dispatcher()
        self.action.dispatcher._ready = False
        self.action.actionManager = ActionMangaer()
        self.action.actionManager._action = Action()

    def test_act(self):
        result = self.action.act()
        assert result == ("normal", self.action)
        self.action.dispatcher._ready = True
        result = self.action.act()
        assert self.action.actionManager.wanted == ("normal", "operator")
        assert self.action.actionManager._action.actSeen


class Test_Append:

    def setup(self):
        Append.__bases__ = (AbstractAction,)
        self.action = Append()
        self.action.cursor = Cursor()
        self.action.actionManager = ActionMangaer()
        self.action.actionManager._action = Action()

    def test_act(self):
        result = self.action.act()
        assert self.action.cursor.gettingSeen
        assert self.action.cursor.finalPosition == (1, 2)
        assert self.action.actionManager.wanted == ("insert", "inserting")
        assert result == ("insert", self.action.actionManager._action)


class TestInsert:

    def setup(self):
        Insert.__bases__ = (AbstractAction,)
        self.action = Insert()
        self.action.cursor = Cursor()
        self.action.actionManager = ActionMangaer()
        self.action.actionManager._action = Action()

    def test_act(self):
        result = self.action.act()
        assert self.action.cursor.finalPosition == (1, 1)
        assert self.action.actionManager.wanted == ("insert", "inserting")
        assert result == ("insert", self.action.actionManager._action)



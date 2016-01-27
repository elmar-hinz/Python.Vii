import curses, os
from .Dispatcher import Dispatcher
from .view.View import View
from .WindowManager import WindowManager
from .ActionManager import ActionManager
from .RegisterManager import RegisterManager
from .Setup import insertCommandMap, normalCommandMap
from .Setup import operatorPendingCommandMap, gCommandMap

os.environ.setdefault('ESCDELAY', '25')

class App:
    def __init__(self, screen):
        screen.nodelay(0)
        windowManager = WindowManager(screen, View(screen))
        dispatcher = Dispatcher()
        actionManager = ActionManager()
        registerManager = RegisterManager()
        actionManager.addMap("normal", normalCommandMap)
        actionManager.addMap("insert", insertCommandMap)
        actionManager.addMap("operatorPending", operatorPendingCommandMap)
        actionManager.addMap("gPending", gCommandMap)
        actionManager.dispatcher = dispatcher
        actionManager.registerManager = registerManager
        actionManager.windowManager = windowManager
        dispatcher.windowManager = windowManager
        dispatcher.actionManager = actionManager

        self.loop(screen, dispatcher)

    def loop(self, screen, dispatcher):
        while True:
            dispatcher.step(screen.get_wch())

def main(): curses.wrapper(App)

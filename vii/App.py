import curses, os
from .Dispatcher import Dispatcher
from .WindowManager import WindowManager
from .ActionManager import ActionManager
from .RegisterManager import RegisterManager
from .Variables import Variables
from .Setup import insertCommandMap, normalCommandMap
from .Setup import operatorPendingCommandMap, gCommandMap
from .Setup import commandCommandMap
from .Range import Position

os.environ.setdefault('ESCDELAY', '25')

class App:
    def __init__(self, screen):
        screen.nodelay(0)
        screen.refresh()
        windowManager = WindowManager()
        cPort = windowManager.createCommandPort(screen)
        windowManager.commandLine = windowManager.createWindow(cPort)
        port = windowManager.createPort(screen)
        windowManager.window = windowManager.createWindow(port)
        windowManager.window.cursor.position(Position(0,0))
        globalVariables = Variables()
        dispatcher = Dispatcher()
        actionManager = ActionManager()
        registerManager = RegisterManager()
        actionManager.addMap("normal", normalCommandMap)
        actionManager.addMap("command", commandCommandMap)
        actionManager.addMap("insert", insertCommandMap)
        actionManager.addMap("operatorPending", operatorPendingCommandMap)
        actionManager.addMap("gPending", gCommandMap)
        actionManager.dispatcher = dispatcher
        actionManager.registerManager = registerManager
        actionManager.windowManager = windowManager
        actionManager.globalVariables = globalVariables
        dispatcher.windowManager = windowManager
        dispatcher.actionManager = actionManager

        self.loop(screen, dispatcher)

    def loop(self, screen, dispatcher):
        while True:
            dispatcher.step(screen.get_wch())

def main(): curses.wrapper(App)

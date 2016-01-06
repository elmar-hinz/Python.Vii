import curses, os
from .Dispatcher import Dispatcher
from .view.View import View
from .WindowManager import WindowManager
from .CommandCatcher import CommandCatcher
from .ActionManager import ActionManager
from . import NormalActions
from .Setup import commandMap

os.environ.setdefault('ESCDELAY', '25')

class App:
    def __init__(self, screen):
        screen.nodelay(0)
        windowManager = WindowManager(screen, View(screen))
        commandCatcher = CommandCatcher(commandMap)
        dispatcher = Dispatcher()
        actionManager = ActionManager()
        actionManager.addMap("normal", commandMap)
        actionManager.addModule("normal", NormalActions)
        actionManager.dispatcher = dispatcher
        actionManager.windowManager = windowManager
        dispatcher.windowManager = windowManager
        dispatcher.actionManager = actionManager

        self.loop(screen, dispatcher)

    def loop(self, screen, dispatcher):
        while True:
            dispatcher.step(screen.getch())

def main(): curses.wrapper(App)

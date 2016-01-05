import curses, os
from .Controller import Controller
from .view.View import View
from .WindowManager import WindowManager
from .CommandCatcher import CommandCatcher
from .Setup import commandMap
from .Shared import Shared

os.environ.setdefault('ESCDELAY', '25')
Shared.modus = "normal"

class Application:
    def __init__(self, screen):
        screen.nodelay(0)
        windowManager = WindowManager(screen, View(screen))
        commandCatcher = CommandCatcher(commandMap)
        controller = Controller(windowManager, commandCatcher)
        self.loop(screen, controller)

    def loop(self, screen, controller):
        while True:
            controller.step(screen.getch())

def main(): curses.wrapper(Application)

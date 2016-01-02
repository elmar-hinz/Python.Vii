import curses, os
from .NormalMode import NormalMode
from .view.View import View

os.environ.setdefault('ESCDELAY', '25')

class Application:
    def __init__(self, screen):
        screen.nodelay(0)
        self.loop(screen, NormalMode(
            View(screen)))

    def loop(self, screen, mode):
        while True:
            mode.handleKey(screen.getch())

def main(): curses.wrapper(Application)

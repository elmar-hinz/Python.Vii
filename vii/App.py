import curses, os
from .NormalMode import NormalMode
from .view.View import View
from .Buffer import Buffer

os.environ.setdefault('ESCDELAY', '25')

class Application:
    def __init__(self, screen):
        screen.nodelay(0)
        self.loop(screen, NormalMode(
            View(screen),Buffer()))

    def loop(self, screen, mode):
        while True:
            mode.step(screen.getch())

def main(): curses.wrapper(Application)

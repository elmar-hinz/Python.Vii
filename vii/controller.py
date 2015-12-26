
class Controller:
    def __init__(self, app):
        self.app = app

    def loop(self):
        self.app.screen.nodelay(1)
        while True:
            if self.app.screen.getch() == ord('q'): break

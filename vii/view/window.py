from .abstractwindow import AbstractWindow

class Window(AbstractWindow):

    def __init__(self, parentWindow):
        super().__init__(parentWindow)

    def layout(self, parentWindow):
        height, width = parentWindow.getmaxyx()
        x, y = 0, 0
        return (height - 1, width, y, x)



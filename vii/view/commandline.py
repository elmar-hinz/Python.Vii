from .abstractwindow import AbstractWindow

class CommandLine(AbstractWindow):

    def layout(self, parentWindow):
        height, width = 1, parentWindow.getmaxyx()[1]
        x, y = 0, parentWindow.getmaxyx()[0] - 1
        return (height, width, y, x)


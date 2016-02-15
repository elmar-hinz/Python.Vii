from ..Setup import numberBarWidth
from ..Range import Range
import curses
from ..Signals import slot
from ..Logger import debug

class Port:

    def __init__(self, parentWindow):
        self.port = curses.newwin(*self.layout(parentWindow))
        self.port.refresh()
        self.maxY, self.maxX = self.port.getmaxyx()

    def layout(self, parentWindow):
        height, width = parentWindow.getmaxyx()
        x, y = 0, 0
        return (height - 1, width, y, x)

    def move(self, y, x):
        self.port.move(y-1, x-1)
        self.port.refresh()

    def draw(self, string):
        self.port.clear()
        self.port.addstr(string[:-1])
        self.port.refresh()

    def clear(self):
        self.port.clear()

    def appendLine(self, line):
        self.port.addstr(line + "\n")

    def refresh(self):
        self.port.refresh()

    def height(self):
        return self.maxY

    def width(self):
        return self.maxX

class WindowLines:

    def splitLines(self, string, width):
        self.lines = []
        def splitLineByNumber(line, number):
            if line == "": yield "\n"
            while line:
                yield line[:number] +"\n"
                line = line[number:]
        for count, line in enumerate(string.splitlines()):
            parts = list(splitLineByNumber(line, width))
            self.lines.append(parts)

    def makeNumbers(self, width):
        self.numbers = []
        format = "%"+str(width-1)+"d "
        for count, line in enumerate(self.lines):
            parts = []
            parts.append(format % (count + 1))
            for i in range(len(line) - 1):
                parts.append(numberBarWidth * " ")
            self.numbers.append(parts)

    def mapPositionFromWindowLines(self, y, x):
        """ y, x are based 1 """
        """ set y, x based 0 """
        y, x = y - 1, x - 1
        if self.lines == []: return (0, 0)
        ySum, xSum, lineY, lineX = 0, 0, -1, -1
        while ySum - 1 < y:
            lineY += 1
            try:
                ySum += len(self.lines[lineY])
            except IndexError:
                return None
        yExcess = ySum - y
        parts = self.lines[lineY][0:-yExcess]
        for part in parts: xSum += len(part) - 1
        lineX = xSum + x
        """ return based 1 """
        return (lineY + 1, lineX + 1)

    def mapPositionToWindowLines(self, y, x):
        """ Both positions, the cursor side and
        the window lines side are based 1. """
        if self.lines == []: return (1,1)
        if x == 0: raise Exception()
        yCount, xCount = 0, 0
        for nr in range(0, y-1):
            yCount += len(self.lines[nr])
        line = self.lines[y-1]
        for i in range(0, len(line)):
            """ For each part x is shortened by part's length """
            part = line[i].rstrip()
            yCount += 1
            if x <= len(part):
                return (yCount, x)
            elif i == len(line) - 1:
                """ On last linebreak """
                x = len(part) + 1
                return (yCount, x)
            else:
                xCount += len(part)
                x -= len(part)
        raise Exception("Never reached")


    def subStringWithNumbers(self, top, hight):
        top = top - 1
        parts = []
        for l in range(len(self.lines)):
            number = self.numbers[l]
            line = self.lines[l]
            for p in range(len(line)):
                parts.append(number[p] + line[p])
        return ''.join(parts[top: top + hight])

    def __str__(self):
        string = ""
        for line in self.lines: string += "".join(line)
        return string

class Window:

    def __init__(self):
        slot("updatedBuffer", self)
        slot("cursorMoved", self)
        self.firstLine = 1

    def makeLines(self):
        width = self.port.width() - 1 - numberBarWidth
        string = str(self.buffer)
        self.lines.splitLines(string, width)
        self.lines.makeNumbers(numberBarWidth)

    def firstWindowLine(self):
        y = self.firstLine
        y, x = self.lines.mapPositionToWindowLines(y,1)
        return y

    def linesAbovePort(self, nr):
        return self.firstLine - nr

    def linesBelowPort(self, nr):
        y, x = nr, self.buffer.lengthOfLine(nr)
        # y below port
        yTarget, xTarget = self.lines.mapPositionToWindowLines(y, x)
        yTop = yTarget - self.port.height() + 1

        topLineY, topLineX = self.lines.mapPositionFromWindowLines(yTop, 1)
        return topLineY - self.firstLine

    def mapWindowLineToPort(self, y):
        top = self.firstWindowLine()
        return y - top + 1

    def movePortTopTo(self, y):
        self.firstLine = y

    def movePortBottomTo(self, y):
        pass

    def draw(self):
        string = self.lines.subStringWithNumbers(
                self.firstWindowLine(), self.port.height())
        self.port.draw(string)

    def move(self):
        y, x = self.cursor.position().toPositionTuple()
        if y == 0: y = 1
        if x == 0: x = 1
        above = self.linesAbovePort(y)
        if above > 0:
            self.firstLine -= above
        else:
            below = self.linesBelowPort(y)
            if below > 0: self.firstLine += below
        self.draw()
        y, x = self.lines.mapPositionToWindowLines(y,x)
        y = self.mapWindowLineToPort(y)
        x += numberBarWidth
        self.port.move(y, x)

    def receive(self, signal, sender, *args):
        self.makeLines()
        self.draw()
        self.move()


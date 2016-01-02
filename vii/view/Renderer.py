from ..Setup import numberBarWidth
from ..Logger import *

def render(buffer):
    format = "\n%"+str(numberBarWidth-1)+"d %s"
    out = ""
    for lineNumber in range(buffer.countOfLines()):
        line = buffer.copyLines(lineNumber, 1)
        out += format % (lineNumber, line)
    out = out[1:]
    return out


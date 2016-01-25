from ..Setup import numberBarWidth
from ..Logger import *
from ..Range import Range

def render(buffer):
    format = "\n%"+str(numberBarWidth-1)+"d %s"
    out = ""
    for lineNumber in range(1, buffer.countOfLines()+1):
        line = buffer.copy(Range(lineNumber, lineNumber))
        if line[-1] == "\n": line = line[:-1]
        out += format % (lineNumber, line)
    out = out[1:]
    return out


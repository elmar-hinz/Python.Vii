from ..config import numberBarWidth
from ..logger import *

def render(buffer):
    format = "\n%"+str(numberBarWidth-1)+"d %s"
    out = ""
    for lineNumber in range(buffer.length()):
        line = buffer[lineNumber]
        out += format % (lineNumber, line)
    out = out[1:]
    return out


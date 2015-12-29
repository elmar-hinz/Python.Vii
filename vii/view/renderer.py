from ..logger import *

def render(buffer):
    out = ""
    for lineNumber in range(buffer.length()):
        line = buffer[lineNumber]
        out += "\n " + str(lineNumber) + " " + str(line)
    out = out[1:]
    return out


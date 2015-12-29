from ..logger import *

def render(buffer):
    debug("Render: buffer length: %s" % buffer.length())
    out = ""
    for lineNumber in range(buffer.length()):
        line = buffer[lineNumber]
        out += "\n " + str(lineNumber) + " " + str(line)
    out = out[1:]
    return out


from .Range import Range, Position
from .Logger import *
import builtins, re

class SearchResult:
    def __init__(self):
        self.position = None
        self.string = None

    def __str__(self):
        return self.string

    def __repr__(self):
        return "%s,%s:'%s'"%( self.position.firstY(),
                self.position.firstX(), self.string)

class Search:
    def __init__(self):
        self.buffer = None

    def search(self, pattern, range, limit = None):
        buffer = self.buffer
        range = buffer._resolveRange(range)
        debug(range)
        pattern = re.compile(pattern)
        results = []
        for y in builtins.range(range.firstY(), range.lastY() + 1):
            startX, stopX = 1, buffer.lengthOfLine(y)
            if y == range.lastY(): endX = range.lastX()
            line = buffer.copy(Range(y, y))
            for hit in re.finditer(pattern, line):
                result = SearchResult()
                result.string = hit.group()
                x = hit.start() + 1
                debug(Position(y, x))
                if range.contains(Position(y,x)):
                    debug("Yes")
                    result.position = Position(y, x)
                    results.append(result)
        if limit: results = results[:limit]
        debug(results)
        return results


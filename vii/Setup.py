normalCommandMap = """
$: EndOfLine
^: BeginningOfLine
A: AppendToLine
I: InsertBeforeLine
a: Append
h: Left
i: Insert
j: Down
k: Up
l: Right
y: Yank
d: Delete
c: Change
idle: Idle
"""

operatorPendingMap = """
$: EndOfLine
^: BeginningOfLine
h: Left
j: Down
k: Up
l: Right
yank: Yank
delete: Delete
change: Change
"""

insertCommandMap = """
inserting: Inserting
"""

"""Window"""
application = "Vii"
numberBarWidth = 5

"""Logging"""
import logging
logPath = "."
logFileName = "vii.log"
logFormat = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
logLevel = logging.DEBUG


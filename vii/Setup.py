normalCommandMap = """
$: EndOfLine
^: BeginningOfLine
a: Append
A: AppendToLine
c: Change
d: Delete
h: Left
i: Insert
I: InsertBeforeLine
j: Down
k: Up
l: Right
p: PutAfter
P: PutBefore
y: Yank
Y: YankLines
idle: Idle
"""

operatorPendingMap = """
$: EndOfLine
^: BeginningOfLine
h: Left
j: Down
k: Up
l: Right
y: YankLines
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


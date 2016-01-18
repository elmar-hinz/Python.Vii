normalCommandMap = """
0: BeginningOfLine
$: EndOfLine
^: BeginningOfLine
a: Append
A: AppendToLine
c: Change
d: Delete
G: GotoLine
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
0: BeginningOfLine
$: EndOfLine
^: BeginningOfLine
c: ChangeLines
d: DeleteLines
g: GotoLine
G: GotoLine
h: Left
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

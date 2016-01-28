normalCommandMap = """
0: vii.Actions.BeginningOfLine
$: vii.Actions.EndOfLine
^: vii.Actions.BeginningOfLine
a: vii.Actions.Append
A: vii.Actions.AppendToLine
c: vii.Actions.Change
C: vii.Actions.ChangeLines
d: vii.Actions.Delete
D: vii.Actions.DeleteLines
g: vii.Actions.GCommand
G: vii.Actions.GotoLine
h: vii.Actions.Left
i: vii.Actions.Insert
I: vii.Actions.InsertBeforeLine
j: vii.Actions.Down
J: vii.Actions.JoinLinesWithAdjustments
k: vii.Actions.Up
l: vii.Actions.Right
p: vii.Actions.PutAfter
P: vii.Actions.PutBefore
x: vii.Actions.DeleteCharacters
X: vii.Actions.DeleteCharactersBefore
y: vii.Actions.Yank
Y: vii.Actions.YankLines
idle: vii.Actions.Idle
"""

operatorPendingCommandMap = """
0: vii.Actions.BeginningOfLine
$: vii.Actions.EndOfLine
^: vii.Actions.BeginningOfLine
c: vii.Actions.ChangeLines
d: vii.Actions.DeleteLines
g: vii.Actions.GCommand
G: vii.Actions.GotoLine
h: vii.Actions.Left
h: vii.Actions.Left
j: vii.Actions.Down
k: vii.Actions.Up
l: vii.Actions.Right
y: vii.Actions.YankLines
"""

gCommandMap = """
g: vii.GActions.GotoTop
J: vii.GActions.JoinLinesWithoutAdjustments
"""

insertCommandMap = """
inserting: vii.Actions.Inserting
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


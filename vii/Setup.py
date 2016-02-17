normalCommandMap = """
0: vii.Actions.BeginningOfLine
$: vii.Actions.EndOfLine
^: vii.Actions.BeginningOfLine
colon: vii.Actions.CommandLine
;: vii.Actions.RepeatFindInLine
,: vii.Actions.RepeatFindInLineInversed
a: vii.Actions.Append
A: vii.Actions.AppendToLine
b: vii.Actions.BackWord
B: vii.Actions.BackWORD
c: vii.Actions.Change
C: vii.Actions.ChangeLines
d: vii.Actions.Delete
D: vii.Actions.DeleteLines
e: vii.Actions.EndOfWord
E: vii.Actions.EndOfWORD
f: vii.Actions.FindInLine
F: vii.Actions.FindInLineBackwards
g: vii.Actions.GCommand
G: vii.Actions.GotoLine
h: vii.Actions.Left
i: vii.Actions.Insert
I: vii.Actions.InsertBeforeLine
j: vii.Actions.Down
J: vii.Actions.JoinLinesWithAdjustments
k: vii.Actions.Up
l: vii.Actions.Right
o: vii.Actions.OpenLineBelow
O: vii.Actions.OpenLineAbove
p: vii.Actions.PutAfter
P: vii.Actions.PutBefore
r: vii.Actions.ReplaceCharacters
s: vii.Actions.SubstituteCharacters
S: vii.Actions.ChangeLines
t: vii.Actions.FindInLineCharacterBefore
T: vii.Actions.FindInLineBackwardsCharacterBefore
x: vii.Actions.DeleteCharacters
X: vii.Actions.DeleteCharactersBefore
w: vii.Actions.Word
W: vii.Actions.WORD
y: vii.Actions.Yank
Y: vii.Actions.YankLines
idle: vii.Actions.Idle
"""

operatorPendingCommandMap = """
0: vii.Actions.BeginningOfLine
$: vii.Actions.EndOfLine
^: vii.Actions.BeginningOfLine
b: vii.Actions.BackWord
B: vii.Actions.BackWORD
c: vii.Actions.ChangeLines
d: vii.Actions.DeleteLines
e: vii.Actions.EndOfWord
E: vii.Actions.EndOfWORD
f: vii.Actions.FindInLine
F: vii.Actions.FindInLineBackwards
g: vii.Actions.GCommand
G: vii.Actions.GotoLine
h: vii.Actions.Left
j: vii.Actions.Down
k: vii.Actions.Up
l: vii.Actions.Right
w: vii.Actions.Word
W: vii.Actions.WORD
y: vii.Actions.YankLines
"""

insertCommandMap = """
inserting: vii.Actions.Inserting
"""

commandCommandMap = """
inserting: vii.Actions.InsertingCommandLine
"""

gCommandMap = """
g: vii.GActions.GotoTop
J: vii.GActions.JoinLinesWithoutAdjustments
e: vii.GActions.EndOfWordBackwards
E: vii.GActions.EndOfWORDBackwards
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



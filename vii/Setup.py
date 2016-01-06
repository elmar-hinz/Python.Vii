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
idle: Idle
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


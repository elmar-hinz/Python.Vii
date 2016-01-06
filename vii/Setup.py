commandMap = """
$: endOfLine
^: beginningOfLine
A: appendToLine
I: insertBeforeLine
a: append
h: left
i: insert
j: down
k: up
l: right
idle: idle
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


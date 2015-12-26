import logging
from vii.config import logPath, logFileName, logFormat, logLevel

fileHandler = logging.FileHandler("{0}/{1}".format(logPath, logFileName))
fileHandler.setFormatter(logging.Formatter(logFormat))

logger = logging.getLogger()
logger.addHandler(fileHandler)
logger.setLevel(logLevel)



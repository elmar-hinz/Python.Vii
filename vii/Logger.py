import logging
from vii.Setup import logPath, logFileName, logFormat, logLevel

fileHandler = logging.FileHandler("{0}/{1}".format(logPath, logFileName))
fileHandler.setFormatter(logging.Formatter(logFormat))

logger = logging.getLogger()
logger.addHandler(fileHandler)
logger.setLevel(logLevel)

def debug(str): logger.debug(str)
def info(str): logger.info(str)
def warn(str): logger.warn(str)
def error(str): logger.error(str)
def critical(str): logger.critical(str)


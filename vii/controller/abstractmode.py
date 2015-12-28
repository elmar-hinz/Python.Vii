from .. logger import logger

class AbstractMode:

    def __init__(self, controller):
        self.controller = controller

    def handleKey(self, key):
        logger.debug(key)

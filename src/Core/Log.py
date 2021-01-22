import logging
from colorlog import ColoredFormatter


class Log:
    logger = None

    @staticmethod
    def Init():
        Log.logger = logging.getLogger(__name__)
        Log.logger.setLevel(logging.DEBUG)

        coloredFormatter = ColoredFormatter(
            "%(log_color)s%(asctime)s CORE: %(message)s%(reset)s", "%H:%M:%S"
        )

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(coloredFormatter)

        Log.logger.addHandler(streamHandler)

    @staticmethod
    def GetLogger():
        return Log.logger

    @staticmethod
    def Trace(message):
        Log.GetLogger().debug(message)

    @staticmethod
    def Info(message):
        Log.GetLogger().info(message)

    @staticmethod
    def Warn(message):
        Log.GetLogger().warn(message)

    @staticmethod
    def Error(message):
        Log.GetLogger().error(message)

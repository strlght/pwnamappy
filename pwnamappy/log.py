import sys
import logging

FORMATTER = logging.Formatter('\r[%(asctime)s] %(message)s', '%H:%M:%S')


class Logger:
    def __init__(self, output=sys.stdout, level=logging.INFO):
        handler = logging.StreamHandler(stream=output)
        handler.setFormatter(FORMATTER)
        self._logger = logging.getLogger('pwnamappyLog')
        self._logger.setLevel(level)
        self._logger.addHandler(handler)

    def info(self, message):
        self._logger.info(message)

    def verbose(self, message):
        self._logger.debug(message)

    def error(self, message):
        self._logger.error(message)

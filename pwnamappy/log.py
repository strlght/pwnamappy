import sys


class Logger:
    def __init__(self, output=sys.stdout, level=0):
        self._output = output
        self._level = level

    def _log(self, level, message):
        print(message, file=self._output)

    def info(self, message):
        self._log(0, message)

    def verbose(self, message):
        self._log(0, message)

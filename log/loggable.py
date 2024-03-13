# logging_abc.py
from abc import ABC
from loguru import logger

import sys

class Loggable(ABC):
    def _log(self, level, message):
        # Automatically binds the class name to the log message
        class_name = self.__class__.__name__
        logger.bind(class_name=class_name).log(level, message)
        
    def info(self, *args):
        message = ' '.join(str(arg) for arg in args)
        self._log("INFO", message)
        
    def warning(self, *args):
        message = ' '.join(str(arg) for arg in args)
        self._log("WARNING", message)
        
    def error(self, *args):
        message = ' '.join(str(arg) for arg in args)
        self._log("ERROR", message)
        
    def debug(self, *args):
        message = ' '.join(str(arg) for arg in args)
        self._log("DEBUG", message)

    def critical(self, *args):
        message = ' '.join(str(arg) for arg in args)
        message += " - Recovery not possible. Exiting..."
        self._log("CRITICAL", message)
        sys.exit() # Kills the program
        
    def bus_debug(self, *args):
        message = ' '.join(str(arg) for arg in args)
        self._log("BUSDEBUG", message)
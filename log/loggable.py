from abc import ABC
from typing import Any, Literal, NoReturn
from loguru import logger

import sys

class Loggable(ABC):
    def _log(self, level: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"], message: str) -> None:
        """Log the specified  message at the specified level on behalf of the class inheriting 
        this ABC
        :param level: The log level for this message
        :type level: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
        :param message: The message to log
        :type message: str
        """
        # Automatically binds the class name to the log message
        class_name = self.__class__.__name__
        logger.bind(class_name=class_name).log(level, message)
        
    def info(self, *args: Any) -> None:
        """Log an info message to loguru
        """
        message = ' '.join(str(arg) for arg in args)
        self._log("INFO", message)
        
    def warning(self, *args: Any) -> None:
        """Log a warning message to loguru
        """
        message = ' '.join(str(arg) for arg in args)
        self._log("WARNING", message)
        
    def error(self, *args: Any) -> None:
        """Log an error message to loguru
        """
        message = ' '.join(str(arg) for arg in args)
        self._log("ERROR", message)
        
    def debug(self, *args: Any) -> None:
        """Log a debug message to loguru
        """
        message = ' '.join(str(arg) for arg in args)
        self._log("DEBUG", message)

    def critical(self, *args: Any) -> NoReturn:
        """Log a critical, unrecoverable error to loguru. 
        Calling this method ends the program

        :return: Nothing
        :rtype: NoReturn
        """
        message = ' '.join(str(arg) for arg in args)
        message += " - Recovery not possible. Exiting..."
        self._log("CRITICAL", message)
        sys.exit() # Kills the program
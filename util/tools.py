import time
import os
from typing import Dict

class Tools:
    @staticmethod
    def safe_get(expression) -> str | None:
        try:
            return eval(expression)
        except Exception:
            return None

    @staticmethod
    def file_exists(path: str) -> bool:
        """Determines whether a file exists (by path)

        :param path: The path to the file
        :type path: str
        :return: True if the file exists
        :rtype: bool
        """
        return os.path.exists(path)
    
    @staticmethod
    def touch(path: str) -> None:
        """Create an empty file at the specified path, if it exists,
        leave it alone

        :param path: The path of the file to create
        :type path: str
        """
        with open(path, 'a'):
            os.utime(path, None)

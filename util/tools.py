import time
import os
from typing import Dict

class Tools:
    def get_user_input_json():
        input_lines = []
        while True:
            line = input()
            if line == "":
                break
            input_lines.append(line)
        return "\n".join(input_lines)

    def merge_json(obj1, obj2):
        for key in obj2:
            obj1[key] = obj2[key] #type:ignore
        return obj1
    
    def stringify_steam_ids(data):
        if isinstance(data, dict):  # If the current element is a dictionary
            for key, value in data.items():
                if key == 'steam_id':
                    data[key] = str(value)
                else:
                    Tools.stringify_steam_ids(value)  # Recurse into the value
        elif isinstance(data, list):  # If the current element is a list
            for item in data:
                Tools.stringify_steam_ids(item)  # Recurse into each item
        # Base case: if data is neither a dict nor a list, do nothing
        return data

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

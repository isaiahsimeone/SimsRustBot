import time

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
            obj1[key] = obj2[key]
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
    
    """
    Seconds since unix epoch (1970)
    """
    def epoch():
        return int(time.time())
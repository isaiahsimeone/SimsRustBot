

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
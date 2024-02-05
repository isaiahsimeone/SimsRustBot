class Tools:
    def get_user_input_json():
        input_lines = []
        while True:
            line = input()
            if line == "":
                break
            input_lines.append(line)
        return "\n".join(input_lines)


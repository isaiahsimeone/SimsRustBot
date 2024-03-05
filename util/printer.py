import sys
from termcolor import cprint, colored
from datetime import datetime

class Printer:
    @classmethod
    def _print(cls, level, message, colour, attrs, file, sep, end, flush):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"{timestamp} [{level}] "
        lines = sep.join(map(str, message)).split('\n')
        formatted_lines = [lines[0]] + [f"{' ' * len(prefix)}{line}" for line in lines[1:]]

        for line in formatted_lines:
            cprint(f"{prefix}{line}" if line is lines[0] else line, colour, attrs=attrs, file=file, end='\n')

        if flush:
            file.flush()

    @classmethod
    def print(cls, level, *args, sep=' ', end='\n', flush=False, file=None):
        if level == 'info':
            colour, attrs = 'white', None
            file = file or sys.stdout
        elif level == 'error':
            colour, attrs = 'red', ['bold']
            file = file or sys.stderr
        elif level == 'prompt':
            colour, attrs = 'yellow', ['reverse']
            file = file or sys.stderr
        elif level == 'warn':
            colour, attrs = 'yellow', None
            file = file or sys.stderr
        else:
            raise ValueError("Invalid log level")

        cls._print(level.upper(), args, colour, attrs, file, sep, end, flush)

    @staticmethod
    def print_banner():
        art = [
            "                                                            \n"
            "  ____  _               ____            _   ____        _   \n"
            " / ___|(_)_ __ ___  ___|  _ \ _   _ ___| |_| __ )  ___ | |_ \n"
            " \___ \| | '_ ` _ \/ __| |_) | | | / __| __|  _ \ / _ \| __|\n"
            "  ___) | | | | | | \__ \  _ <| |_| \__ \ |_| |_) | (_) | |_ \n"
            " |____/|_|_| |_| |_|___/_| \_\\\__,_|___/\__|____/ \___/ \__|\n"
            "------------------------------------------------------------\n"
        ]
        rainbow_colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
        for line in art:
            colored_line = ''
            for i, char in enumerate(line):
                # Cycle through the rainbow colors
                color = rainbow_colors[i % len(rainbow_colors)]
                # Add colored character to the line
                colored_line += colored(char, color) # type: ignore
            print(colored_line)

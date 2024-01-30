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
    def print_info(cls, *args, colour='white', attrs=None, file=sys.stdout, sep=' ', end='\n', flush=False):
        cls._print('INFO', args, colour, attrs or [], file, sep, end, flush)

    @classmethod
    def print_error(cls, *args, file=sys.stderr, sep=' ', end='\n', flush=True):
        cls._print('ERROR', args, 'red', ['bold'], file, sep, end, flush)

    @classmethod
    def print_prompt(cls, *args, file=sys.stderr, sep=' ', end='\n', flush=True):
        cls._print('PROMPT', args, 'yellow', ['reverse'], file, sep, end, flush)

    @classmethod
    def print_warning(cls, *args, file=sys.stderr, sep=' ', end='\n', flush=True):
        cls._print('WARN', args, 'yellow', None, file, sep, end, flush)

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
                colored_line += colored(char, color)
            print(colored_line)

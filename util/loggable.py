class Loggable:
    def __init__(self, log_function):
        self.log_function = log_function

    def log(self, *args, type="info"):
        message = ' '.join(str(arg) for arg in args)
        prefix = self.__class__.__name__  # Get the class name as prefix
        full_message = f"[{prefix}]: {message}"
        self.log_function(full_message, type)
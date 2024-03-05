from .command import Command

class CommandRegistry:
    commands = {}

    @classmethod
    def register_command(cls, command):
        instance = command()  # Instantiate the command
        for alias in instance.get_aliases():
            cls.commands[alias] = instance
        return command  # Return the class, not the instance

def command(cls):
    """Decorator to register commands."""
    CommandRegistry.register_command(cls)
    return cls
from .command_registry import CommandRegistry
import difflib

from util.loggable import Loggable

class CommandExecutor(Loggable):
    def __init__(self, rust_api, command_prefix):
        self.prefix = command_prefix[0]
        self.api = rust_api
        super().__init__(rust_api.log)
        
    async def parse_and_execute_command(self, message, sender_steam_id):
        if not message.startswith(self.prefix):
            return "" # Not a command

        # Remove the leader and split the input into components
        components = message[len(self.prefix):].split()
        if not components:
            return "" # not a command

        # The first component is the command name, the rest are arguments
        command_name, *args = components
        
        # Find and execute the command
        command = CommandRegistry.commands.get(command_name.lower())
        if command:
            self.log(f"Executing command '{command}' with args {args}")
            await command.execute(self.api, sender_steam_id, args)
        else:
            self.log(f"Unknown command '{command_name}'. Did you mean '{self.suggest_closest_match(command_name)}'?", type="warn")
            return "?:" + str(command_name) + ":" + str(self.suggest_closest_match(command_name))
        
        return ""
        
        # levenshtein distance
    def suggest_closest_match(self, command_name):
        """
        Levenshtein distance to determine which command is closest
        to a provided one (excluding itself)
        """
        # Get a list of all possible names and aliases
        all_names = list(CommandRegistry.commands.keys())
        # Use difflib to find the closest match(es)
        closest_matches = difflib.get_close_matches(command_name.lower(), all_names, n=1, cutoff=0.3)
        if closest_matches:
            return closest_matches[0]  # Return the closest match
        return "idk"  # No close match found
    
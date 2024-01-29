import json
import os

class ConfigManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        """Load the configuration file."""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def save_config(self):
        """Save the current configuration to the file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.config, file, indent=4)

    def get(self, key, default=None):
        """Get a value from the configuration."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a value in the configuration."""
        self.config[key] = value
        self.save_config()

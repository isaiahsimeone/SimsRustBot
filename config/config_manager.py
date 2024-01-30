import json
import os

class ConfigManager:
    def __init__(self, config_path, default_config=None):
        self.config_path = config_path
        self.default_config = default_config or {}
        self.config_data = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path) and os.path.getsize(self.config_path) > 0:
            try:
                with open(self.config_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {self.config_path}. Using default config.")
        return self.default_config.copy()

    def save_config(self):
        try:
            with open(self.config_path, 'w') as file:
                json.dump(self.config_data, file, indent=4)
        except IOError as e:
            print(f"Error: Unable to write to config file {self.config_path}: {e}")

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()

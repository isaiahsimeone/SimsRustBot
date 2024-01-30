import json
import os
from util.printer import Printer
from util.tools import Tools

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

    def reload_get(self, key, default=None):
        self.config_data = self.load_config()
        return self.get(key, default=default)

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()

    def validate_json(self, input_data, required_fields):
        try:
            data = json.loads(input_data) or {}
            if not required_fields.issubset(data.keys()):
                missing = required_fields - data.keys()
                Printer.print_error(f"Missing fields in JSON data: {missing}")
                return None
            return data
        except json.JSONDecodeError as e:
            Printer.print_error(f"Invalid JSON: {e}")
            return None
        except TypeError as e:
            Printer.print_error(f"There is a problem with config.json {e}")
            return None

    def validate_fcm(self, input_data):
        return self.validate_json(input_data, {"desc", "id", "img", "ip", "logo", "name", "playerId", "playerToken", "port", "type", "url"})

    
    def check_fcm_credentials(self):
        if self.validate_fcm(json.dumps(self.get("fcm_credentials"))):
            Printer.print_info("FCM Credentials found, and I think they look valid")
            return None
        
        Printer.print_error("FCM Credentials weren't found in ./config/config.json (or are incorrect)\n"
                                "To obtain these credentials, you can use the Rustplus.py Link Companion browser extension for Google Chrome\n\n"
                                "Available here: https://chromewebstore.google.com/detail/rustpluspy-link-companion/gojhnmnggbnflhdcpcemeahejhcimnlf \n\n"
                                "Either input your credentials into ./config/config.json, or paste them here. Press enter once finished. \n")
        while True:
            Printer.print_prompt("Enter your FCM credentials: \n")
            fcm_credentials_json = Tools.get_user_input_json()
            try:
                fcm_credentials_dict = json.loads(fcm_credentials_json)
            except json.JSONDecodeError as e:
                Printer.print_error(f"Invalid JSON: {e}")
                continue
            
            # Check if the config.json file has been updated by the user
            config_has_valid_fcm = self.validate_fcm(json.dumps(self.reload_get("fcm_credentials")))
            if config_has_valid_fcm:
                Printer.print_info("FCM Credentials found in config.json. Continuing")
                return None
            
            # Check if what the user entered are valid FCM creds. If they are, save them
            is_valid_fcm = self.validate_fcm(json.dumps(fcm_credentials_dict))
            if is_valid_fcm:
                Printer.print_info("These seem like valid FCM credentials. Saving to config.json")
                self.set("fcm_credentials", fcm_credentials_dict)
                self.save_config()
                return None
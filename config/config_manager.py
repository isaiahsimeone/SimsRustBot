import json
import os
from util.printer import Printer
from util.tools import Tools

class ConfigManager:
    def __init__(self, config_path, default_config=None):
        self.config_path = config_path
        self.default_config = default_config or {}
        
        self.generate_initial_config_if_absent()
        
        self.config_data = self.load_config()
        

    def load_config(self):
        if os.path.exists(self.config_path) and os.path.getsize(self.config_path) > 0:
            try:
                with open(self.config_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                Printer.print("warn", f"Could not decode JSON from {self.config_path}. Using default config.")
        return self.default_config.copy()

    def save_config(self):
        try:
            with open(self.config_path, 'w') as file:
                json.dump(self.config_data, file, indent=4)
        except IOError as e:
            Printer.print("error", f"Unable to write to config file {self.config_path}: {e}")

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
                Printer.print("error", f"Missing fields in JSON data: {missing}")
                return None
            return data
        except json.JSONDecodeError as e:
            Printer.print("error", f"Invalid JSON: {e}")
            return None
        except TypeError as e:
            Printer.print("error", f"There is a problem with config.json {e}")
            return None

    def validate_fcm(self, input_data):
        return self.validate_json(input_data, {"fcm_credentials", "expo_push_token", "rustplus_auth_token"})
    
    def validate_server_details(self, input_data):
        return self.validate_json(input_data, {"desc", "id", "img", "ip", "logo", "name", "playerId", "playerToken", "port", "type", "url"})
    
    def check_fcm_credentials(self):
        if self.validate_fcm(json.dumps(self.get("fcm_credentials"))):
            Printer.print("info", "FCM credentials found, and I think they look valid")
            return None
        
        Printer.print("error", "FCM credentials weren't found in ./config/config.json (or are incorrect)\n"
                                "To obtain these credentials, you can use the Rustplus.py Link Companion browser extension for Google Chrome\n\n"
                                "Available here: https://chromewebstore.google.com/detail/rustpluspy-link-companion/gojhnmnggbnflhdcpcemeahejhcimnlf \n\n"
                                "Paste the topmost field. Either input your credentials into ./config/config.json, or paste them here. Press enter once finished. \n")
        while True:
            Printer.print("prompt", "Enter your FCM credentials: \n")
            fcm_credentials_json = Tools.get_user_input_json()
            try:
                fcm_credentials_dict = json.loads(fcm_credentials_json)
            except json.JSONDecodeError as e:
                Printer.print("error", f"Invalid JSON: {e}")
                continue
            
            # Check if the config.json file has been updated by the user
            config_has_valid_fcm = self.validate_fcm(json.dumps(self.reload_get("fcm_credentials")))
            if config_has_valid_fcm:
                Printer.print("info", "FCM credentials found in config.json. Continuing")
                return None
            
            # Check if what the user entered are valid FCM creds. If they are, save them
            is_valid_fcm = self.validate_fcm(json.dumps(fcm_credentials_dict))
            if is_valid_fcm:
                Printer.print("info", "These seem like valid FCM credentials. Saving to config.json")
                self.set("fcm_credentials", fcm_credentials_dict)
                self.save_config()
                return None
            
    def check_server_details(self):
        if self.validate_server_details(json.dumps(self.get("server_details"))):
            Printer.print("info", "Server details found, and I think they look valid")
            return None
        
        Printer.print("error", "Server details weren't found in ./config/config.json (or are incorrect)\n"
                                "To obtain these details, you can use the Rustplus.py Link Companion browser extension for Google Chrome\n\n"
                                "Available here: https://chromewebstore.google.com/detail/rustpluspy-link-companion/gojhnmnggbnflhdcpcemeahejhcimnlf \n\n"
                                "Paste the bottom-most field. Either input the details into ./config/config.json, or paste them here. Press enter once finished. \n")
        while True:
            Printer.print("prompt", "Enter your server details: \n")
            server_details_json = Tools.get_user_input_json()
            try:
                server_details_dict = json.loads(server_details_json)
            except json.JSONDecodeError as e:
                Printer.print("error", f"Invalid JSON: {e}")
                continue
            
            # Check if the config.json file has been updated by the user
            config_has_valid_fcm = self.validate_server_details(json.dumps(self.reload_get("server_details")))
            if config_has_valid_fcm:
                Printer.print("info", "Server details found in config.json. Continuing")
                return None
            
            # Check if what the user entered are valid server details. If they are, save them
            is_valid_fcm = self.validate_server_details(json.dumps(server_details_dict))
            if is_valid_fcm:
                Printer.print("info", "These seem like valid server details. Saving to config.json")
                self.set("server_details", server_details_dict)
                self.save_config()
                return None
    
    def generate_initial_config_if_absent(self):
        default_config = {
            "fcm_credentials": {
                
            },
            "server_details": {
                
            },
            "database": {
                "path": "database/db.db"
            },
            "discord": {
                "enabled": "true",
                "logging_enabled": "true",
                "bot_token": "",
                "notification_channel": "",
                "chat_channel": ""
            },
            "web": {
                "host": "localhost",
                "port": "5000",
                "logging_enabled": "true"
            },
            "rust": {
                "map_polling_frequency_seconds": {
                    "marker": "60",
                    "event": "10"
                }
            }
        }

        config_needs_update = False

        if os.path.isfile(self.config_path):
            try:
                with open(self.config_path, 'r') as config_file:
                    existing_config = json.load(config_file)
                    for key in default_config.keys():
                        if key not in existing_config:
                            existing_config[key] = default_config[key]
                            config_needs_update = True
            except json.JSONDecodeError:
                existing_config = default_config
                config_needs_update = True

            if config_needs_update:
                with open(self.config_path, 'w') as config_file:
                    json.dump(existing_config, config_file, indent=4)
                Printer.print("info", "Configuration file updated with missing fields. Creating...")
            else:
                Printer.print("info", "Configuration file already exists and is up to date.")
        else:
            with open(self.config_path, 'w') as config_file:
                json.dump(default_config, config_file, indent=4)
            Printer.print("info", "Initial configuration generated.")
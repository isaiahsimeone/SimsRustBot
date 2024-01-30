import asyncio
import sys
from messenger import Messenger
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from config.config_manager import ConfigManager
from util.printer import Printer

def main():
    Printer.print_banner()
    
    config = ConfigManager("./config/config.json")   

    messenger = Messenger(config)
    
    if not config.get("rust_plus_credentials"):
        Printer.print_error("FCM Credentials weren't found in ./config/config.json !!!\n"
                            "To obtain these credentials, you can use the Rustplus.py Link Companion browser extension for Google Chrome\n"
                            "Available here: https://chromewebstore.google.com/detail/rustpluspy-link-companion/gojhnmnggbnflhdcpcemeahejhcimnlf \n\n"
                            "Either input your credentials into ./config/config.json, or paste them here now: \n")
        return None
   
    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)
    

    sys.stdout.flush()


if __name__ == "__main__":
    sys.stdout.flush()
    main()
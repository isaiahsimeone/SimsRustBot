import asyncio
import sys
from messenger import Messenger
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from config.config_manager import ConfigManager

def main():
    config_manager = ConfigManager()   

    messenger = Messenger(config_manager)
    
    if not config.get("fcm_credentials"):
        print("Need FCM credentials. Use rustplus companion chrome plugin")
   
    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)
    

    sys.stdout.flush()


if __name__ == "__main__":
    sys.stdout.flush()
    main()
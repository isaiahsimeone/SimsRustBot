import asyncio
import sys
from messenger import Messenger
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from web.fcm_registration import FCMRegistration
from config_manager import ConfigManager

def main():
    #config = ConfigManager("./config.json")   
    config = None
    messenger = Messenger(config)
    
    #if not config.get("fcm_credentials"):
    FCMRegistration(messenger).register_with_fcm()
   
    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)
    

    sys.stdout.flush()


if __name__ == "__main__":
    sys.stdout.flush()
    main()
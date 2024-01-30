import asyncio
import sys
import json
from messenger import Messenger
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from config.config_manager import ConfigManager
from util.printer import Printer
from util.tools import Tools

def main():
    Printer.print_banner()
    
    config = ConfigManager("./config/config.json")
    config.check_fcm_credentials()
   
    messenger = Messenger(config)
   
    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)
    


if __name__ == "__main__":
    main()
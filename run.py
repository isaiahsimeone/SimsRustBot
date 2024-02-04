import asyncio
import sys
import json
import threading

from ipc.messenger import Messenger
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from config.config_manager import ConfigManager
from util.printer import Printer
from util.tools import Tools
from database.database import init_db

def main():
    Printer.print_banner()
    
    config = ConfigManager("./config/config.json")
    config.check_fcm_credentials()
    config.check_server_details()
   
    init_db(config)
   
    messenger = Messenger(config)

    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)

    # Create threads for each service
    rustplus_thread = threading.Thread(target=start_service_threaded, args=(rustplus_api,))
    discord_thread = threading.Thread(target=start_service_threaded, args=(discord_bot,))
    web_server_thread = threading.Thread(target=start_service_threaded, args=(web_server,))

    # Start threads
    rustplus_thread.start()
    discord_thread.start()
    web_server_thread.start()

    # Join thread
    rustplus_thread.join()
    discord_thread.join()
    web_server_thread.join()

    
def start_service_threaded(service):
    Printer.print("info", "Starting thread for", service)
    service.execute()


if __name__ == "__main__":
    main()
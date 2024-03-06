
import argparse
import os
import threading
import unittest

from ipc.bus import BUS
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from config.config_manager import ConfigManager
from util.printer import Printer
from util.tools import Tools
from database.database import Database

def main():
    Printer.print_banner()
    
    parser = argparse.ArgumentParser(description="Run the application or tests")
    parser.add_argument('--test', action='store_true', help="Run tests instead of the application")
    args = parser.parse_args()
    
    # If --test is specified, run tests
    if args.test:
        run_tests()
        return
    
    database = Database()
    
    config = ConfigManager("./config/config.json")
    config.check_fcm_credentials()
    config.check_server_details()
   
    bus = BUS(config, database)

    rustplus_api = RustPlusAPI(bus)
    discord_bot = DiscordBot(bus)
    web_server = WebServer(bus)

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

def run_tests():
    # This will load all test cases from the tests directory
    # Adjust the pattern or directory as needed
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='./tests', pattern='*_test.py')
    print(suite)
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    main()
import asyncio
from rustplus import RustSocket

from messenger import Messenger
from rustplus_api import RustPlusAPI
from discord_bot import DiscordBot
from web import WebServer

def main():
    messenger = Messenger()
    
    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)



if __name__ == "__main":
    main()
import asyncio
import sys
from messenger import Messenger
from rustplus_api.rust_plus_api import RustPlusAPI
from discord_bot.discord_bot import DiscordBot
from web.web_server import WebServer
from fcm_registration import FCMRegistration

def main():
    messenger = Messenger()

    fcm_registration = FCMRegistration(messenger)

    rustplus_api = RustPlusAPI(messenger)
    discord_bot = DiscordBot(messenger)
    web_server = WebServer(messenger)

    sys.stdout.flush()


if __name__ == "__main__":
    sys.stdout.flush()
    main()
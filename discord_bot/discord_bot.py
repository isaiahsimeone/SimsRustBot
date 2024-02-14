from ipc.bus import BUS, Service
from ipc.message import Message, MessageType
import discord
import asyncio

class DiscordBot:
    def __init__(self, BUS):
        self.BUS = BUS
        self.config = self.BUS.get_config().get("discord")
        self.bot = None
    
    # entry point

    def execute(self):
        self.discord_bot_token = self.get_bot_token()
        self.log("No token was entered, so no discord bot will be started" if self.discord_bot_token is None else "Bot token found. Attempting to start Discord bot")
        
        self.BUS.subscribe(Service.DISCORD, self.process_message)
        self.log("Discord Bot subscribed for messages")
        
        self.start_bot(self.discord_bot_token)
        
    def start_bot(self, token):
        intents = discord.Intents.all()
        intents.message_content = True
        self.bot = discord.Client(intents=intents)
        
        # Set up event handlers
        from .bot_event_handlers import setup_event_handlers
        setup_event_handlers(self.bot, self)
        
        if self.config.get("logging_enabled") == "true":
            self.log("Discord library logging is disabled")
            self.bot.run(token, log_handler=None)
        else:
            self.bot.run(token)

    def get_bot_token(self):
        bot_token = self.config.get("bot_token")
        
        if not bot_token:
            self.log_synchronous("ERROR: I don't have a discord bot token! Enter one, or leave blank")
            token = input("Enter discord bot token: ").strip()
            if token == "":
                return None
            else:
                self.config.set("bot_token", token)
                return token
        return bot_token
        
    async def process_message(self, message: Message, sender):
        pass
        #self.log("Got message: " + message + " from " + str(sender))
    
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.DISCORD, message, target_service_id)
    
    def log(self, message: Message):
        self.BUS.log(Service.DISCORD, message)
        
    def log_synchronous(self, message: Message):
        self.BUS.log(Service.DISCORD, message)
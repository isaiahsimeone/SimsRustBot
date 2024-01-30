from messenger import Messenger, Service
import discord


class DiscordBot:
    def __init__(self, messenger):
        self.messenger = messenger
    
    # entry point
    def run(self):
        self.discord_bot_token = self.get_bot_token()
        self.log("No token was entered, so no discord bot will be started" if self.discord_bot_token is None else "Bot token found. Attempting to start Discord bot")
        
        self.start_bot(self.discord_bot_token)
        
        self.messenger.subscribe(Service.DISCORD, self.process_message)
        self.log("Discord Bot subscribed for messages")
    
    def start_bot(self, token):
        intents = discord.Intents.all()
        intents.message_content = True
        self.bot = discord.Client(intents=intents)
        if self.messenger.get_config().get("discord_disable_lib_logging") == "true":
            self.log("Discord library logging is disabled")
            self.bot.run(token, log_handler=None)
        else:
            self.bot.run(token)

    def get_bot_token(self):
        bot_token = self.messenger.get_config().get("discord_bot_token")
        
        if not bot_token:
            self.log("ERROR: I don't have a discord bot token! Enter one, or leave blank")
            token = input("Enter discord bot token: ").strip()
            if token == "":
                return None
            else:
                self.messenger.get_config().set("discord_bot_token", token)
                return token
        return bot_token
        
    def process_message(self, message):
        pass
    
    def send_message(self, message):
        self.messenger.send_message(Service.DISCORD, message)
        
    def log(self, message):
        self.messenger.log(Service.DISCORD, message)
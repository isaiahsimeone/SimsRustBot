

class DiscordBotEventHandlers(Loggable):
    def __init__(self, bot, discord_bot):
        self.bot = bot
        self.discord_bot = discord_bot
        super().__init__(discord_bot.log)

    async def on_ready(self):
        await self.discord_bot.BUS.block_until_subscribed(service_id=Service.DISCORD, wait_for=Service.RUSTAPI)
        self.log(f"{self.bot.user} is ready.")

    async def on_connect(self):
        self.log(f"{self.bot.user} connected to Discord!")

    async def on_disconnect(self):
        self.log(f"{self.bot.user} disconnected from Discord")
        
    async def on_message(self, message):
        if message.content.startswith("!"):
            await message.channel.send("HI!")
            self.discord_bot.send_message(message.content)

def setup_event_handlers(bot, discord_bot):
    handlers = DiscordBotEventHandlers(bot, discord_bot)
    bot.event(handlers.on_ready)
    bot.event(handlers.on_connect)
    bot.event(handlers.on_disconnect)
    bot.event(handlers.on_message)

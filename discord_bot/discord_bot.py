from messenger import Messenger, Service

class DiscordBot:
    def __init__(self, messenger):
        self.messenger = messenger
        self.messenger.subscribe(Service.DISCORD, self.process_message)
        self.messenger.log(Service.DISCORD, "Discord Bot subscribed for messages")
        
    def process_message(self, message):
        pass
    
    def send_message(self, message):
        self.messenger.send_message(Service.DISCORD, message)
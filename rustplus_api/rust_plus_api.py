from messenger import Messenger, Service
from rustplus import *


class RustPlusAPI:
    def __init__(self, messenger):
        self.messenger = messenger
        self.config = messenger.get_config()

    # entry point
    def run(self):
        self.messenger.subscribe(Service.RUSTAPI, self.process_message)
        self.log("Rust Service subscribed for messages")
        
        self.log("Attempting to connect to RustPlus")
        
        ip = self.config.get("fcm_credentials").get("ip")
        port = self.config.get("fcm_credentials").get("port")
        #steamid = self.config.get("steam_id")
        playerId = self.config.get("fcm_credentials").get("playerId")
        
        print(ip, port, "A", playerId)
        
        #socket = RustSocket()
        
    def process_message(self, message):
        pass
    
    def send_message(self, message):
        self.messenger.send_message(Service.RUSTAPI, message)
        
    def log(self, message):
        self.messenger.log(Service.RUSTAPI, message)
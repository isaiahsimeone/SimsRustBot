from messenger import Messenger, Service

class RustPlusAPI:
    def __init__(self, messenger):
        self.messenger = messenger
        self.messenger.subscribe(Service.RUSTAPI, self.process_message)
        self.messenger.log(Service.RUSTAPI, "Rust Service subscribed for messages")
        
    def process_message(self, message):
        pass
    
    def send_message(self, message):
        self.messenger.send_message(Service.RUSTAPI, message)
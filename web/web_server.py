from messenger import Messenger, Service

class WebServer:
    def __init__(self, messenger):
        self.messenger = messenger
        self.messenger.subscribe(Service.WEBSERVER, self.process_message)
        self.messenger.log(Service.WEBSERVER, "Web Server subscribed for messages")
        
    def process_message(self, message):
        pass
    
    def send_message(self, message):
        self.messenger.send_message(Service.WEBSERVER, message)
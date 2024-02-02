from messenger import Messenger, Service
from flask import Flask
import logging
import threading
from .web_routes import setup_routes

app = Flask(__name__)
app.secret_key = 'secret'

class WebServer:
    def __init__(self, messenger):
        self.messenger = messenger
        self.config = self.messenger.get_config().get("web")
        if self.config.get("logging_enabled") != "true":
            self.log("Werkzeug logging is disabled")
            logger = logging.getLogger('werkzeug')
            logger.setLevel(logging.ERROR)

        self.port = self.config.get("port")
        self.host = self.config.get("host")

    def execute(self):
        setup_routes(app, self)  # Set up routes with the WebServer instance
        
        self.log(f"Web Server started at http://{self.host}:{self.port}")
        self.messenger.subscribe(Service.WEBSERVER, self.process_message)
        self.log("Web Server subscribed for messages")
        
        threading.Thread(target=lambda: app.run(host=self.host, port=self.port, debug=True, use_reloader=False)).start()

    def process_message(self, message, sender):
        self.log("Got message: " + message + " from " + str(sender))

    def send_message(self, message, target_service_id=None):
        self.messenger.send_message(Service.WEBSERVER, message, target_service_id)

    def log(self, message):
        self.messenger.log(Service.WEBSERVER, message)

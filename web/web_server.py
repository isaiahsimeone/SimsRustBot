from messenger import Messenger, Service
from flask import Flask
import logging
import threading
from .web_routes import setup_routes

app = Flask(__name__)
app.secret_key = 'secret'

# Only show errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class WebServer:
    def __init__(self, messenger):
        self.messenger = messenger
        self.config = self.messenger.get_config()
        if self.config.get("werkzeug_disable_logging") == "true":
            self.log("Werkzeug logging is disabled")
            logger = logging.getLogger('werkzeug')
            logger.setLevel(logging.ERROR)

        self.port = self.config.get("web_server_port", 4000)
        self.host = self.config.get("web_server_host", '127.0.0.1')

    def run(self):
        setup_routes(app, self)  # Set up routes with the WebServer instance
        threading.Thread(target=lambda: app.run(host=self.host, port=self.port, debug=True, use_reloader=False)).start()
        self.log(f"Web Server started at http://{self.host}:{self.port}")
        self.messenger.subscribe(Service.WEBSERVER, self.process_message)
        self.log("Web Server subscribed for messages")

    def process_message(self, message):
        pass

    def send_message(self, message):
        self.messenger.send_message(Service.WEBSERVER, message)

    def log(self, message):
        self.messenger.log(Service.WEBSERVER, message)

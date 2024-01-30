from messenger import Messenger, Service
from flask import Flask, render_template, request, session, redirect, url_for
import logging

app = Flask(__name__)
app.secret_key = 'secret'

# Only show errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class WebServer:
    def __init__(self, messenger):
        self.messenger = messenger
        if messenger.get_config().get("werkzeug_disable_logging") == "true":
            self.log("Werkzeug logging is disabled")
            logger = logging.getLogger('werkzeug')
            logger.setLevel(logging.ERROR)

    # entry point
    def run(self):
        # start web server
        app.run(port=4000)
        self.messenger.subscribe(Service.WEBSERVER, self.process_message)
        self.log("Web Server subscribed for messages")
        
    def process_message(self, message):
        pass
    
    def send_message(self, message):
        self.messenger.send_message(Service.WEBSERVER, message)
        
    def log(self, message):
        self.messenger.log(Service.WEBSERVER, message)
    
    @app.route('/')
    def index():
        return render_template("index.html")
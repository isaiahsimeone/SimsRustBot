from messenger import Messenger, Service
from flask import Flask, render_template, request, session, redirect, url_for
import uuid

app = Flask(__name__)
app.secret_key = 'secret'

class WebServer:

    
    def __init__(self, messenger):
        self.messenger = messenger

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
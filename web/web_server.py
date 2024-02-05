from ipc.messenger import Messenger, Service
from ipc.message import Message, MessageType
from flask import Flask, url_for
import logging
import threading
from .web_routes import setup_routes
import json
from PIL import Image 

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
    
    async def process_message(self, message, sender):
        msg = json.loads(message)
        
        #print("WEBS GOT MESSAGE:", message)
        if msg.get("type") == MessageType.RUST_SERVER_MAP.value:
            self.log("Got server map. Moving to images root")
            #print(msg)
            image_data = msg.get("data").get("data")
            
            img_width = image_data.get("width")
            img_height = image_data.get("height")
            img_pixels = [tuple(pixel) for pixel in image_data.get("pixels")]
            
            img = Image.new(mode="RGB", size=(img_width, img_height))
            img.putdata(img_pixels)
            
            img.save("web/static/images/map.jpg")
            
                
        #self.log("Got message: " + message + " from " + str(sender))

    async def send_message(self, message: Message, target_service_id=None):
        await self.messenger.send_message(Service.WEBSERVER, message, target_service_id)

    def log(self, message):
        self.messenger.log(Service.WEBSERVER, message)

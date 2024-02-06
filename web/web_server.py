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
        
        self.map_markers_queue = []

    def execute(self):
        setup_routes(app, self)  # Set up routes with the WebServer instance
        
        self.log(f"Web Server started at http://{self.host}:{self.port}")
        self.messenger.subscribe(Service.WEBSERVER, self.process_message)
        self.log("Web Server subscribed for messages")
        
        threading.Thread(target=lambda: app.run(host=self.host, port=self.port, debug=True, use_reloader=False)).start()
    
    def update_map_markers(self, markers_data):
        self.map_markers_queue.append(markers_data)
        
        
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
            
        if msg.get("type") == MessageType.RUST_MAP_MARKERS.value:
            self.log("Updating map markers")
            data = msg.get("data")
            # MAP SHOULD BE UPDATED WITH MARKERS HERE
            data['markers'].insert(0, 3000) # TODO: Make not hardcoded
            self.update_map_markers(data.get("markers"))
            
                
        #self.log("Got message: " + message + " from " + str(sender))

    async def send_message(self, message: Message, target_service_id=None):
        await self.messenger.send_message(Service.WEBSERVER, message, target_service_id)

    def log(self, message):
        self.messenger.log(Service.WEBSERVER, message)

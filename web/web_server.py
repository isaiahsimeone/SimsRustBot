from ipc.messenger import Messenger, Service
from ipc.message import Message, MessageType
from flask import Flask, url_for
import logging
import threading
from .web_routes import setup_routes
from .web_event_streams import setup_event_streams
from .message_executor import MessageExecutor
import json
import asyncio

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
        
        self.steam_api_key = self.config.get("steam_api_key")
        
        self.executor = MessageExecutor(self)
        
        self.map_markers_queue = []
        self.team_update_queue = []
        self.map_monuments = None
        self.map_info = None

    def execute(self):
        asyncio.run(self.webserver_main())
    
    async def webserver_main(self):
        # Setup routes and event streams
        setup_routes(app, self)
        setup_event_streams(app, self)
        
        
        self.messenger.subscribe(Service.WEBSERVER, self.process_message)
        self.log("Web Server subscribed for messages")
        
        await self.messenger.block_until_subscribed(service_id=Service.WEBSERVER, wait_for=Service.RUSTAPI)
        
        threading.Thread(target=lambda: app.run(host=self.host, port=self.port, debug=True, use_reloader=False)).start()
        
        self.log(f"Web Server started at http://{self.host}:{self.port}")
        
        asyncio.create_task(self.request_rust_data())
        
        await asyncio.Future()
        
        
        
    # get the map image, get server info, start marker polling
    async def request_rust_data(self):
        
        # Request map info
        self.log("Requesting Map Info")
        await self.send_message(Message(MessageType.REQUEST_RUST_MAP_INFO, {}), target_service_id=Service.RUSTAPI)
        
        # Request map image 
        self.log("Requesting Server Map")
        await self.send_message(Message(MessageType.REQUEST_RUST_SERVER_MAP, {}), target_service_id=Service.RUSTAPI)
        
        # Request monuments
        self.log("Requesting Server Monuments")
        await self.send_message(Message(MessageType.REQUEST_RUST_MAP_MONUMENTS, {}), target_service_id=Service.RUSTAPI)

    def get_host(self):
        return self.host
    
    def get_port(self):
        return self.port
    
    def get_steam_api_key(self):
        return self.steam_api_key
        
    async def process_message(self, message, sender):
        msg = json.loads(message)
        await self.executor.execute_message(msg, sender)

    async def send_message(self, message: Message, target_service_id=None):
        await self.messenger.send_message(Service.WEBSERVER, message, target_service_id)

    def log(self, message):
        self.messenger.log(Service.WEBSERVER, message)

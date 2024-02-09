from ipc.messenger import Messenger, Service
from ipc.message import Message, MessageType

from rustplus import RustSocket, ChatEvent, CommandOptions
import asyncio
from .FCM_listener import FCM
from .map_poller import MapPoller
from .event_listener import EventListener

from .commands.send_message import send_message as rust_send_message
from .commands.get_server_info import get_server_info
from .commands.get_server_map import get_server_map

from .message_executor import MessageExecutor

import json

class RustPlusAPI:
    def __init__(self, messenger):
        self.messenger = messenger
        self.config = messenger.get_config()
        self.server = self.config.get("server_details").get("ip")
        self.port = self.config.get("server_details").get("port")
        self.steamID = self.config.get("server_details").get("playerId")
        self.playerToken = self.config.get("server_details").get("playerToken")
        self.socket = RustSocket(self.server, self.port, self.steamID, self.playerToken)
        self.event_listener = None
    
    # entry point
    def execute(self):
        asyncio.run(self.api_main())


    async def api_main(self):
        self.log("Connecting to Rust Server (" + self.server + ")...")
        await self.socket.connect()
        self.log("Connected to Rust Server! (" + self.server + ")")

        self.executor = MessageExecutor(self)
        self.messenger.subscribe(Service.RUSTAPI, self.process_message)
        self.log("Rust Service subscribed for messages")
        
        self.log("Starting FCM listener...")
        FCM(self.config.get("fcm_credentials")).start()
        self.log("FCM Listener startup complete")

        self.log("Fetching server info...")
        await get_server_info(self.socket)
        #self.log("Downloading server map...")


        # Register event listener
        self.event_listener = EventListener(self.socket, self.messenger)
        self.log("Event listener setup complete")
        
        poll_rate = self.messenger.get_config().get("rust").get("map_polling_frequency_seconds")
        self.map_poller = MapPoller(self.socket, self.messenger)
        
        # Start map marker polling
        asyncio.create_task(self.map_poller.start_marker_polling())
        self.log("Map marker polling started with a frequency of " + poll_rate + " seconds")
      
        
        #DEBUG
        self.log("Got Server Info: " + str(await self.socket.get_info()))
         
        await asyncio.Future() # Keep running
        
        self.log("Exiting...")
        
    def get_socket(self):
        return self.socket

    async def disconnect_api(self):
        self.log("Disconnecting from Rust Server (" + self.server + ")...")
        await self.socket.disconnect()
        self.log("Disconnected from Rust Server (" + self.server + ")")

    async def process_message(self, msg, sender):
        msg = json.loads(msg)
        await self.executor.execute_message(msg, sender)

    async def send_message(self, message: Message, target_service_id=None):
        await self.messenger.send_message(Service.RUSTAPI, message, target_service_id)

    def log(self, message):
        self.messenger.log(Service.RUSTAPI, message)

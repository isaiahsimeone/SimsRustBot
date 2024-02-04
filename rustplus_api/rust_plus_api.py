from messenger import Messenger, Service
from rustplus import RustSocket, ChatEvent, CommandOptions
import asyncio
from .FCM_listener import FCM

from .event_listners import *

from .commands.send_message import send_message as rust_send_message
from .commands.get_server_info import get_server_info
from .commands.get_server_map import get_server_map

class RustPlusAPI:
    def __init__(self, messenger):
        self.messenger = messenger
        self.config = messenger.get_config()
        self.server = self.config.get("server_details").get("ip")
        self.port = self.config.get("server_details").get("port")
        self.steamID = self.config.get("server_details").get("playerId")
        self.playerToken = self.config.get("server_details").get("playerToken")
        self.socket = RustSocket(self.server, self.port, self.steamID, self.playerToken)

    # entry point
    def execute(self):
        self.messenger.subscribe(Service.RUSTAPI, self.process_message)
        self.log("Rust Service subscribed for messages")

        asyncio.run(self.api_main())

    async def api_main(self):
        self.log("Connecting to Rust Server (" + self.server + ")...")
        await self.socket.connect()
        self.log("Connected to Rust Server! (" + self.server + ")")

        self.log("Starting FCM listener...")
        FCM(self.config.get("fcm_credentials")).start()
        self.log("FCM Listener startup complete")

        self.log("Fetching server info...")
        await get_server_info(self.socket)
        self.log("Downloading server map...")
        await get_server_map(self.socket)

        # Register event handlers
        self.socket.team_event(team_event_handler)
        self.socket.chat_event(chat_event_handler)
        self.socket.protobuf_received(proto_event_handler)
        self.log("Event handlers setup complete")
        
        await asyncio.Future() # Keep running
        
        self.log("Exiting...")

    async def disconnect_api(self):
        self.log("Disconnecting from Rust Server (" + self.server + ")...")
        await self.socket.disconnect()
        self.log("Disconnected from Rust Server (" + self.server + ")")

    def process_message(self, message, sender):
        self.log("Got message: " + message + " from " + str(sender))

    def send_message(self, message, target_service_id=None):
        self.messenger.send_message(Service.RUSTAPI, message, target_service_id)

    def log(self, message):
        self.messenger.log(Service.RUSTAPI, message)

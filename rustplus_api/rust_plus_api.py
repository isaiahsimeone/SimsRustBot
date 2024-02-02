from messenger import Messenger, Service
from rustplus import RustSocket
import asyncio
from .FCM_listener import FCM
from .commands.send_message import send_message as rust_send_message
from .commands.get_server_info import get_server_info
from .commands.get_server_map import get_server_map

class RustPlusAPI:
    def __init__(self, messenger):
        self.messenger = messenger
        self.config = messenger.get_config()
        self.socket = None
        
        self.server = None
        self.port = None
        self.steamID = None
        self.playerToken = None
         
    # entry point
    def execute(self):
        self.messenger.subscribe(Service.RUSTAPI, self.process_message)
        self.log("Rust Service subscribed for messages")
        
        self.log("Attempting to connect to RustPlus")

        asyncio.run(self.api_main())
        
    async def api_main(self):
        server_details = self.config.get("server_details")
        fcm_credentials = self.config.get("fcm_credentials")
        
        self.server = server_details.get("ip")
        self.port = server_details.get("port")
        self.steamID = server_details.get("playerId")
        self.playerToken = server_details.get("playerToken")
         
        socket = RustSocket(self.server, self.port, self.steamID, self.playerToken)
        self.socket = socket
        
        await self.connect_api()
        
        
        
        self.log("Starting FCM listener...")
        FCM(fcm_credentials).start()
        self.log("FCM Listener startup complete")
        
        self.log("Fetching server info...")
        await get_server_info(self.socket)
        self.log("Downloading server map...")
        await get_server_map(self.socket)

        
    async def speak(self):
        await self.socket.send_team_message("TESTTTxxx")

    async def connect_api(self):
        self.log("Connecting to Rust Server (" + self.server + ")...")
        await self.socket.connect()
        self.log("Connected to Rust Server! (" + self.server + ")")
    
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
from messenger import Messenger, Service
from rustplus import RustSocket
import asyncio

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
        fcm_creds = self.config.get("fcm_credentials")
        
        self.server = fcm_creds.get("ip")
        self.port = fcm_creds.get("port")
        self.steamID = fcm_creds.get("playerId")
        self.playerToken = fcm_creds.get("playerToken")
         
        socket = RustSocket(self.server, self.port, self.steamID, self.playerToken)
        self.socket = socket
        
        await self.connect_api()

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
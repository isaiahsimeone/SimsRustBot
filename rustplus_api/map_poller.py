import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.messenger import Service
from ipc.message import Message, MessageType

class MapPoller:
    def __init__(self, socket, messenger):
        self.socket = socket
        self.messenger = messenger
        self.frequency = int(messenger.get_config().get("rust").get("map_polling_frequency_seconds"))
    
    
    async def start(self):
        while True:
            print("poll map")
            await self.poll_map_markers()
            await self.poll_map_events()
            await asyncio.sleep(self.frequency)
    
    # Listen for explosions, cargo, chinook, locked crates & heli
    async def poll_map_events(self):
        events = await self.socket.get_current_events()
        msg_data = {"events": events}  
        message = Message(MessageType.RUST_MAP_EVENTS, msg_data)
        await self.send_message(message)
    
    async def poll_map_markers(self):
        markers = await self.socket.get_markers()
        msg_data = {"markers": markers}
        message = Message(MessageType.RUST_MAP_MARKERS, msg_data)
        await self.send_message(message)
        
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.messenger.send_message(Service.RUSTAPI, message, target_service_id)
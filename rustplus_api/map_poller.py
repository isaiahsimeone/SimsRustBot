import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.messenger import Service
from ipc.message import Message, MessageType

class MapPoller:
    def __init__(self, socket, messenger):
        self.socket = socket
        self.messenger = messenger
        
        frequencies = messenger.get_config().get("rust").get("map_polling_frequency_seconds")
        self.marker_poll_frequency = int(frequencies.get("marker"))
        self.event_poll_frequency = int(frequencies.get("event"))
    
    
    async def start_marker_polling(self):
        while True:
            print("poll map")
            await self.poll_map_markers()
            await asyncio.sleep(self.marker_poll_frequency)
            
    async def start_event_polling(self):
        while True:
            print("marker poll")
            await self.poll_map_events()
            await asyncio.sleep(self.event_poll_frequency)
    
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